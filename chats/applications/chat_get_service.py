from chats.domains import ChatRepository, Chat
from chats.serializers import ChatObjectResponseSerailzier, JoinedMembersResponseSerializer
from utils.redis_utils import get_redis_connection

class ChatGetService:
    def __init__(self, chat_repository: ChatRepository, *args, **kwargs):
        self._chat_repository = chat_repository

    def get_all_chat_rooms(self):
        redis_conn = get_redis_connection(db_select=1)
        redis_pipe = redis_conn.pipeline()
        chats: list[Chat] = self._chat_repository.find_all_chat_rooms_with_members()
        serialized_chats = ChatObjectResponseSerailzier(chats, many=True).data

        for chat in chats:
            redis_pipe.scard(chat.id)

        headcounts = redis_pipe.execute()

        for chat_data, headcount in zip(serialized_chats, headcounts):
            chat_data['headcount'] = headcount

        return serialized_chats
    
    def get_chat_detail(self, chat_id: int):
        chat: Chat = self._chat_repository.find_chat_by_id(chat_id)
        chat_object_response_serializer = ChatObjectResponseSerailzier(chat)
        return chat_object_response_serializer.data
    
    def get_joined_members(self, chat_id: int):
        redis_conn = get_redis_connection(db_select=1)
        joined_members = list(redis_conn.smembers(chat_id))
        return JoinedMembersResponseSerializer(self._JoinedMembersDto(joined_members)).data

    class _JoinedMembersDto:
        def __init__(self, joined_members: list[int]):
            self.joined_members = joined_members