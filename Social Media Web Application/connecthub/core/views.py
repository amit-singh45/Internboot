from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import CustomUserCreationForm, ProfileForm, PostForm, CommentForm
from .models import CustomUser, Post, Like, Comment, Follow, Notification

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    # personalized feed: posts from users this user follows
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(user__id__in=following_ids).order_by('-created_at')
    # fallback: if no following, show all
    if not posts.exists():
        posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_form = PostForm()
    return render(request, 'home.html', {'page_obj': page_obj, 'post_form': post_form})

@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = user.posts.all().order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts, 'is_following': is_following})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    return redirect('home')

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form})

@login_required
def explore(request):
    # show all posts sorted by likes (trending)
    posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count','-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'explore.html', {'page_obj': page_obj})

@login_required
def notifications_view(request):
    notifs = request.user.notifications.all()[:20]
    return render(request, 'notifications.html', {'notifications': notifs})

@login_required
def leaderboard(request):
    top_followed = CustomUser.objects.annotate(followers_count=Count('following_related')).order_by('-followers_count')[:10]
    top_posts = CustomUser.objects.annotate(posts_count=Count('posts')).order_by('-posts_count')[:10]
    top_likes_users = CustomUser.objects.annotate(likes_received=Count('posts__likes')).order_by('-likes_received')[:10]
    return render(request, 'leaderboard.html', {'top_followed': top_followed, 'top_posts': top_posts, 'top_likes_users': top_likes_users})

@login_required
def follow_toggle(request):
    if request.method == 'POST' and request.user.is_authenticated:
        target_id = request.POST.get('user_id')
        if str(request.user.id) == str(target_id):
            return JsonResponse({'error':'cannot_follow_self'}, status=400)
        target = get_object_or_404(CustomUser, id=target_id)
        obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            obj.delete()
            action = 'unfollowed'
        else:
            # create notification
            Notification.objects.create(recipient=target, sender=request.user, notification_type='follow')
            action = 'followed'
        return JsonResponse({'action': action, 'followers_count': target.following_related.count()})
    return HttpResponseForbidden()

@login_required
def like_toggle(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            action = 'unliked'
        except Like.DoesNotExist:
            Like.objects.create(user=request.user, post=post)
            Notification.objects.create(recipient=post.user, sender=request.user, notification_type='like', post=post)
            action = 'liked'
        return JsonResponse({'action': action, 'like_count': post.likes.count()})
    return HttpResponseForbidden()


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    total_users = CustomUser.objects.count()
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    top_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'top_posts': top_posts,
    })


@login_required
def about(request):
    return render(request, 'about.html')


@login_required

def search_view(request):
    query = request.GET.get('q')
    users = []
    posts = []

    if query:
        users = CustomUser.objects.filter(username__icontains=query)
        posts = Post.objects.filter(content__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }

    return render(request, 'search.html', context)
