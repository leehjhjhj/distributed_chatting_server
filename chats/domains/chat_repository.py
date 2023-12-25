from chats.domains import Chat
from django.shortcuts import get_list_or_404, get_object_or_404

class ChatRepository:
    def save_chat(self, chat: Chat):
        chat.save()
    
    def find_chats_with_members(self):
        return Chat.objects.select_related('made_by').order_by('-created_at')
    
    def find_chats_with_members_by_member_id(self, user_id: int):
        return Chat.objects.filter(made_by_id=user_id).select_related('made_by').order_by('-created_at')
    
    def find_chats_in_chats_with_members_by_member_id(self, chats: list[Chat], user_id: int):
        return chats.filter(made_by_id=user_id)

    def find_chat_by_id(self, chat_id: int):
        return get_object_or_404(Chat, id=chat_id)
    
    def delete_chat_object(self, chat: Chat):
        chat.delete()

    def find_chats_by_search_term(self, search_chat_name: str):
        return Chat.objects.filter(name__search=search_chat_name).select_related('made_by')