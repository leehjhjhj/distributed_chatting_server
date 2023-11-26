from chats.domains import ChatRepository, Chat
from chats.serializers import ChatObjectResponseSerailzier

class ChatGetService:
    def __init__(self, chat_repository: ChatRepository, *args, **kwargs):
        self._chat_repository = chat_repository

    def get_all_chat_rooms(self):
        chats: list[Chat] = self._chat_repository.find_all_chat_rooms()
        all_chat_response_serializer = ChatObjectResponseSerailzier(chats, many=True)
        return all_chat_response_serializer.data
    
    def get_chat_detail(self, chat_id: int):
        chat: Chat = self._chat_repository.find_chat_by_id(chat_id)
        chat_object_response_serializer = ChatObjectResponseSerailzier(chat)
        return chat_object_response_serializer.data