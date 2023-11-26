from chats.domains import Chat
from django.shortcuts import get_list_or_404, get_object_or_404

class ChatRepository:
    def save_chat(self, chat: Chat):
        chat.save()
    
    def find_all_chat_rooms(self):
        return get_list_or_404(Chat)
    
    def find_chat_by_id(self, chat_id: int):
        return get_object_or_404(Chat, id=chat_id)