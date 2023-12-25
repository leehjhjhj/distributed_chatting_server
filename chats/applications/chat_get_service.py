from chats.domains import ChatRepository, Chat
from chats.serializers import ChatObjectResponseSerailzier, JoinedMembersResponseSerializer
from utils.redis_utils import get_redis_connection
from utils.exceptions import RequiredLoginError
from typing import Optional
from django.db import connection, reset_queries

reset_queries()

class ChatGetService:
    def __init__(self, chat_repository: ChatRepository, *args, **kwargs):
        self._chat_repository = chat_repository

    def get_all_chat_rooms(self, order_by: str, search: Optional[str], user_data: dict):
        if search:
            chats = self._chat_repository.find_chats_by_search_term(search)
            if order_by == "my":
                if user_data.is_anonymous:
                    raise RequiredLoginError
                if chats:
                    chats: list[Chat] = self._chat_repository.find_chats_in_chats_with_members_by_member_id(chats, user_data.id)
        else:
            if order_by == "my":
                if user_data.is_anonymous:
                    raise RequiredLoginError
                chats: list[Chat] = self._chat_repository.find_chats_with_members_by_member_id(user_data.id)
            else:
                chats: list[Chat] = self._chat_repository.find_chats_with_members()

        serialized_chats = ChatObjectResponseSerailzier(chats, many=True).data
        serialized_chats_with_headcount = self._attach_headcount_to_serialzier(serialized_chats, chats)
        
        if order_by == "headcount":
            serialized_chats_with_headcount = sorted(serialized_chats_with_headcount, key=lambda x: x['headcount'], reverse=True)
        return serialized_chats_with_headcount
    
    def get_chat_detail(self, chat_id: int):
        chat: Chat = self._chat_repository.find_chat_by_id(chat_id)
        chat_object_response_serializer = ChatObjectResponseSerailzier(chat)
        return chat_object_response_serializer.data
    
    def get_joined_members(self, chat_id: int):
        redis_conn = get_redis_connection(db_select=1)
        joined_members = list(redis_conn.smembers(chat_id))
        return JoinedMembersResponseSerializer(self._JoinedMembersDto(joined_members)).data
    
    def _attach_headcount_to_serialzier(self, serialized_chats: dict, chats: list[Chat]):
        redis_conn = get_redis_connection(db_select=1)
        redis_pipe = redis_conn.pipeline()

        for chat in chats:
            redis_pipe.scard(chat.id)
        headcounts = redis_pipe.execute()

        for chat_data, headcount in zip(serialized_chats, headcounts):
            chat_data['headcount'] = headcount
        return serialized_chats
    
    class _JoinedMembersDto:
        def __init__(self, joined_members: list[int]):
            self.joined_members = joined_members