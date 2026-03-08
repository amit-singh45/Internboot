from django.contrib import admin
from .models import UserProfile, ChatGroup, Message, MessageReaction, Story, PinnedChat, ArchivedChat

class ChatGroupAdmin(admin.ModelAdmin):
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change:
            form.instance.members.add(request.user)
            form.instance.admins.add(request.user)

admin.site.register(UserProfile)
admin.site.register(ChatGroup, ChatGroupAdmin)
admin.site.register(Message)
admin.site.register(MessageReaction)
admin.site.register(Story)
admin.site.register(PinnedChat)
admin.site.register(ArchivedChat)
