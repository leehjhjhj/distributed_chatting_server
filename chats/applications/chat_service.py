from chats.domains import ChatRepository, Participant, Chat
from chats.serializers import ChatCreateRequestSerializer
from members.domains import Member

class ChatService:
    def __init__(self, chat_repository: ChatRepository, *args, **kwargs):
        self._chat_repository = chat_repository

    def create_chat(self, request_data: dict, user_data: Member):
        chat_create_request_serializer = ChatCreateRequestSerializer(data=request_data)
        chat_create_request_serializer.is_valid(raise_exception=True)
        chat_data: dict = chat_create_request_serializer.validated_data

        new_chat: Chat = Chat(
                name=chat_data.get('name'),
                description=chat_data.get('description'),
                made_by=user_data,
                max_capacity=chat_data.get('max_capacity')
                )
        self._chat_repository.save_chat(new_chat)