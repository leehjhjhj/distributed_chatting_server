from chats.domains import Chat
from django.shortcuts import get_list_or_404, get_object_or_404

class ChatRepository:
    def save_chat(self, chat: Chat):
        chat.save()
    
    def find_all_chat_rooms_with_members(self):
        return get_list_or_404(Chat.objects.select_related('made_by').order_by('-created_at'))
    
    def find_chat_by_id(self, chat_id: int):
        return get_object_or_404(Chat, id=chat_id)
    
    def delete_chat_object(self, chat: Chat):
        chat.delete()