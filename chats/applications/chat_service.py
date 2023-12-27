from chats.domains import ChatRepository, Chat
from chats.serializers import ChatCreateRequestSerializer, ChatMessageResponseSerializer, ChatIdResponseSerializer, ChatJoinResponseSerializer
from members.domains import Member
from boto3.dynamodb.conditions import Key
from utils.connect_dynamodb import get_dynamodb_table
from utils.redis_utils import get_redis_connection
from utils.exceptions import OverMaxCountError, NoRightToDeleteChatError

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
        chat_id_serialzier = ChatIdResponseSerializer(self._ChatCreateDto(new_chat.id))
        return chat_id_serialzier.data
    
    def join_chat(self, user_data: Member, chat_id: str):
        chat = self._chat_repository.find_chat_by_id(chat_id)
        max_capacity = chat.max_capacity
        redis_conn = get_redis_connection(db_select=1)
        headcount = redis_conn.scard(chat_id)
        if headcount + 1 > max_capacity:
            raise OverMaxCountError

        table = get_dynamodb_table()
        query_params = {
            'KeyConditionExpression': Key('chat_id').eq(chat_id),
            'ScanIndexForward': False,
            'Limit': 10
        }
        response = table.query(**query_params)
        old_messages = response.get('Items')
        joined_members = list(redis_conn.smembers(chat_id))
        joined_members.append(user_data.nickname)
        last_evaluated_key = response.get('LastEvaluatedKey', None)
        chat_message_response_serialzier = ChatJoinResponseSerializer(self._ChatJoinDto(joined_members, last_evaluated_key, old_messages))
        return chat_message_response_serialzier.data
    
    def get_more_messages(self, chat_id: str, last_evaluated_key: str):
        table = get_dynamodb_table()
        query_params = {
            'KeyConditionExpression': Key('chat_id').eq(chat_id),
            'ScanIndexForward': False,
            'Limit': 10
        }
        if last_evaluated_key is not None:
            exclusive_start_key = {
                "chat_id": chat_id,
                "timestamp": last_evaluated_key
            }
            query_params['ExclusiveStartKey'] = exclusive_start_key
            
        response = table.query(**query_params)
        old_messages = response.get('Items')
        last_evaluated_key = response.get('LastEvaluatedKey', None)
        chat_message_response_serialzier = ChatMessageResponseSerializer(self._ChatResponseDto(old_messages, last_evaluated_key))
        return chat_message_response_serialzier.data
    
    def delete_chat(self, chat_id: int, user_data: dict):
        chat: Chat = self._chat_repository.find_chat_by_id(chat_id)
        if chat.made_by != user_data:
            raise NoRightToDeleteChatError
        self._chat_repository.delete_chat_object(chat)

    class _ChatJoinDto:
        def __init__(self,  joined_members: list, last_evaluated_key: dict, old_messages: list[dict]):
            self.joined_members = joined_members
            self.last_evaluated_key = last_evaluated_key
            self.old_messages = old_messages

    class _ChatResponseDto:
        def __init__(self, old_messages: list[dict], last_evaluated_key: dict):
            self.old_messages = old_messages
            self.last_evaluated_key = last_evaluated_key

    class _ChatCreateDto:
        def __init__(self, chat_id: int):
            self.chat_id = chat_id