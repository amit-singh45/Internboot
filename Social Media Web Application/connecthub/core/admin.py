from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .models import CustomUser, Post, Like, Comment, Follow, Notification

# customize admin site titles
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', admin.site.site_header)
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', admin.site.site_title)
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', admin.site.index_title)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('profile_picture','bio','location')}),
    )

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Notification)
