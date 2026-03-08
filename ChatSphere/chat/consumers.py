import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatGroup, Message, MessageReaction

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_type = self.scope['url_route']['kwargs']['chat_type']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_type}_{self.chat_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'chat_message':
            message = data['message']
            sender_id = self.scope['user'].id

            # Save message to DB asynchronously
            msg_obj = await self.save_message(sender_id, self.chat_type, self.chat_id, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                    'sender_username': self.scope['user'].username,
                    'msg_id': msg_obj.id,
                    'timestamp': msg_obj.created_at.strftime("%H:%M")
                }
            )
        elif action == 'typing':
            # Broadcast typing status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'sender_id': self.scope['user'].id,
                    'is_typing': data.get('is_typing', False)
                }
            )
        elif action == 'message_seen':
            # Mark messages as seen
            msg_ids = data.get('msg_ids', [])
            await self.mark_messages_seen(msg_ids)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'messages_seen',
                    'msg_ids': msg_ids,
                    'sender_id': self.scope['user'].id
                }
            )
        elif action == 'edit_message':
            msg_id = data.get('msg_id')
            new_text = data.get('text')
            await self.edit_message_db(msg_id, self.scope['user'].id, new_text)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_edited',
                    'msg_id': msg_id,
                    'text': new_text
                }
            )
        elif action == 'delete_message':
            msg_id = data.get('msg_id')
            await self.delete_message_db(msg_id, self.scope['user'].id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_deleted',
                    'msg_id': msg_id
                }
            )
        elif action == 'react_message':
            msg_id = data.get('msg_id')
            emoji = data.get('emoji')
            await self.react_message_db(msg_id, self.scope['user'], emoji)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_reacted',
                    'msg_id': msg_id,
                    'emoji': emoji,
                    'user_id': self.scope['user'].id
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'msg_id': event['msg_id'],
            'timestamp': event['timestamp']
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            'action': 'typing',
            'sender_id': event['sender_id'],
            'is_typing': event['is_typing']
        }))

    async def messages_seen(self, event):
        await self.send(text_data=json.dumps({
            'action': 'message_seen',
            'msg_ids': event['msg_ids'],
            'sender_id': event['sender_id'],
        }))

    async def message_edited(self, event):
        await self.send(text_data=json.dumps({
            'action': 'message_edited',
            'msg_id': event['msg_id'],
            'text': event['text']
        }))

    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            'action': 'message_deleted',
            'msg_id': event['msg_id']
        }))

    async def message_reacted(self, event):
        await self.send(text_data=json.dumps({
            'action': 'message_reacted',
            'msg_id': event['msg_id'],
            'emoji': event['emoji'],
            'user_id': event['user_id']
        }))

    @database_sync_to_async
    def save_message(self, sender_id, chat_type, chat_id, text):
        user = User.objects.get(id=sender_id)
        if chat_type == 'private':
            receiver = User.objects.get(id=chat_id)
            return Message.objects.create(sender=user, receiver=receiver, text=text)
        elif chat_type == 'group':
            group = ChatGroup.objects.get(id=chat_id)
            return Message.objects.create(sender=user, chat_group=group, text=text)

    @database_sync_to_async
    def mark_messages_seen(self, msg_ids):
        Message.objects.filter(id__in=msg_ids).update(is_seen=True)

    @database_sync_to_async
    def edit_message_db(self, msg_id, user_id, new_text):
        try:
            msg = Message.objects.get(id=msg_id, sender_id=user_id)
            msg.text = new_text
            msg.edited = True
            msg.save()
        except Message.DoesNotExist:
            pass

    @database_sync_to_async
    def delete_message_db(self, msg_id, user_id):
        try:
            msg = Message.objects.get(id=msg_id, sender_id=user_id)
            msg.deleted = True
            msg.save()
        except Message.DoesNotExist:
            pass

    @database_sync_to_async
    def react_message_db(self, msg_id, user, emoji):
        try:
            msg = Message.objects.get(id=msg_id)
            reaction, created = MessageReaction.objects.get_or_create(message=msg, user=user)
            reaction.emoji = emoji
            reaction.save()
        except Message.DoesNotExist:
            pass

class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.user_id = self.scope['user'].id
            self.room_group_name = 'global_presence'

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.update_user_status(True)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_presence',
                    'user_id': self.user_id,
                    'is_online': True
                }
            )
            
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'user_id'):
            await self.update_user_status(False)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_presence',
                    'user_id': self.user_id,
                    'is_online': False
                }
            )

            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def user_presence(self, event):
        await self.send(text_data=json.dumps({
            'action': 'presence',
            'user_id': event['user_id'],
            'is_online': event['is_online']
        }))

    @database_sync_to_async
    def update_user_status(self, is_online):
        from django.utils import timezone
        user = User.objects.get(id=self.user_id)
        user.profile.is_online = is_online
        if not is_online:
            user.profile.last_seen = timezone.now()
        user.profile.save()
