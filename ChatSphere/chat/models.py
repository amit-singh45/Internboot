from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now_add=True)
    dark_mode_enabled = models.BooleanField(default=True)
    wallpaper = models.ImageField(upload_to='wallpapers/', null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='group_avatars/', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups')
    admins = models.ManyToManyField(User, related_name='admin_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Group: {self.name}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    
    # Message Content
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    file = models.FileField(upload_to='message_files/', null=True, blank=True)
    voice_note = models.FileField(upload_to='voice_notes/', null=True, blank=True)
    
    # Meta data
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    
    # Replies
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    def __str__(self):
        target = self.receiver.username if self.receiver else str(self.chat_group)
        return f"Message from {self.sender.username} to {target}"
        
class MessageReaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'user')

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/', null=True, blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

class PinnedChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pinned_chats')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pinned_by')
    target_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ArchivedChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='archived_chats')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='archived_by')
    target_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
