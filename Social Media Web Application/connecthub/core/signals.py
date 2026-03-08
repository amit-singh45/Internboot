from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment, Follow, Notification

@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.post.user, sender=instance.user, notification_type='like', post=instance.post)

@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.post.user, sender=instance.user, notification_type='comment', post=instance.post)

@receiver(post_save, sender=Follow)
def follow_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(recipient=instance.following, sender=instance.follower, notification_type='follow')
