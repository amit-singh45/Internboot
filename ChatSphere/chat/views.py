from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.models import User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('chat_home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # UserProfile is created via signals
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('chat_home')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat_home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Ensure profile exists before accessing
                if not hasattr(user, 'profile'):
                    from .models import UserProfile
                    UserProfile.objects.create(user=user)

                # Mark user online
                user.profile.is_online = True
                user.profile.save()
                
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('chat_home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'chat/login.html', {'login_form': form})

def logout_view(request):
    if request.user.is_authenticated:
        request.user.profile.is_online = False
        request.user.profile.save()
    logout(request)
    messages.info(request, 'You have successfully logged out.') 
    return redirect('login')

from django.db.models import Q
from .models import ChatGroup, Message, Story
from django.utils import timezone

def chat_home(request, user_id=None, group_id=None):
    if not request.user.is_authenticated:
        return redirect('login')
        
    # Ensure active user has a profile
    if not hasattr(request.user, 'profile'):
        from .models import UserProfile
        UserProfile.objects.create(user=request.user)
        
    users = User.objects.exclude(id=request.user.id).select_related('profile')
    groups = ChatGroup.objects.filter(members=request.user)
    print("DEBUG - Groups for user", request.user, ":", groups)
    recent_stories = Story.objects.filter(expires_at__gte=timezone.now()).select_related('user', 'user__profile')
    
    active_thread = None
    active_group = None
    other_user = None
    messages_list = []
    chat_type = None
    chat_id = None
    
    if user_id:
        other_user = get_object_or_404(User, id=user_id)
        
        messages_list = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) | 
            Q(sender=other_user, receiver=request.user)
        ).select_related('sender', 'sender__profile').order_by('created_at')
        
        # Mark messages as seen for 1-1 chat
        messages_list.exclude(sender=request.user).filter(is_seen=False).update(is_seen=True)
        
        chat_type = 'private'
        chat_id = other_user.id
        
    elif group_id:
        active_group = get_object_or_404(ChatGroup, id=group_id)
        if request.user not in active_group.members.all():
            active_group.members.add(request.user)
            
        messages_list = active_group.messages.all().select_related('sender', 'sender__profile').order_by('created_at')
        chat_type = 'group'
        chat_id = active_group.id
        
    context = {
        'users': users,
        'groups': groups,
        'stories': recent_stories,
        'active_group': active_group,
        'other_user': other_user,
        'messages_list': messages_list,
        'chat_type': chat_type,
        'chat_id': chat_id,
    }
    return render(request, 'chat/chat.html', context)

import json
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def upload_media(request):
    if not request.user.is_authenticated or request.method != 'POST':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    chat_type = request.POST.get('chat_type')
    chat_id = request.POST.get('chat_id')
    text = request.POST.get('text', '')
    
    file_obj = request.FILES.get('file')
    image_obj = request.FILES.get('image')
    voice_obj = request.FILES.get('voice_note')
    
    msg = Message(sender=request.user, text=text)

    if chat_type == 'private':
        msg.receiver = get_object_or_404(User, id=chat_id)
    elif chat_type == 'group':
        msg.chat_group = get_object_or_404(ChatGroup, id=chat_id)
    else:
        return JsonResponse({'error': 'Invalid chat type'}, status=400)
        
    if file_obj:
        msg.file = file_obj
    if image_obj:
        msg.image = image_obj
    if voice_obj:
        msg.voice_note = voice_obj
        
    msg.save()
    
    # Broadcast to channels
    channel_layer = get_channel_layer()
    room_group_name = f'chat_{chat_type}_{chat_id}'
    
    message_data = {
        'type': 'chat_message',
        'message': text,
        'sender_id': msg.sender.id,
        'sender_username': msg.sender.username,
        'msg_id': msg.id,
        'timestamp': msg.created_at.strftime("%H:%M"),
        'image_url': msg.image.url if msg.image else None,
        'file_url': msg.file.url if msg.file else None,
        'voice_url': msg.voice_note.url if msg.voice_note else None,
    }
    
    async_to_sync(channel_layer.group_send)(room_group_name, message_data)
    
    return JsonResponse({'success': True, 'msg_id': msg.id})

def create_group(request):
    if not request.user.is_authenticated or request.method != 'POST':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    name = request.POST.get('name')
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
        
    group = ChatGroup.objects.create(name=name)
    group.admins.add(request.user)
    group.members.add(request.user)
    
    # Add other members if provided (comma separated ids)
    member_ids = request.POST.get('members', '').split(',')
    for mid in member_ids:
        if mid.strip() and mid.strip().isdigit():
            group.members.add(mid.strip())
            
    return JsonResponse({'success': True, 'group_id': group.id})

def update_profile(request):
    if not request.user.is_authenticated or request.method != 'POST':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    profile = request.user.profile
    bio = request.POST.get('bio')
    dark_mode = request.POST.get('dark_mode_enabled')
    avatar = request.FILES.get('avatar')
    wallpaper = request.FILES.get('wallpaper')
    
    if bio is not None:
        profile.bio = bio
    if dark_mode is not None:
        profile.dark_mode_enabled = dark_mode.lower() == 'true'
    if avatar:
        profile.avatar = avatar
    if wallpaper:
        profile.wallpaper = wallpaper
        
    profile.save()
    return JsonResponse({'success': True})

def upload_story(request):
    if not request.user.is_authenticated or request.method != 'POST':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({'error': 'Image is required'}, status=400)
        
    Story.objects.create(user=request.user, image=image)
    return JsonResponse({'success': True})
