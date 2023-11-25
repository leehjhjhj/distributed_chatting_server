from chats.domains import ChatRepository, Participant, Chat
from chats.serializers import ChatCreateRequestSerializer, ChatMessageResponseSerializer, ChatMessageSerializer
from members.domains import Member
from boto3.dynamodb.conditions import Key
from utils.connect_dynamodb import get_dynamodb_table

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

    def join_chat(self, user_data: Member, chat_id: str):
        table = get_dynamodb_table()
        query_params = {
            'KeyConditionExpression': Key('chat_id').eq(chat_id),
            'ScanIndexForward': False,
            'Limit': 20
        }
        response = table.query(**query_params)
        old_messages = response.get('Items')
        chat_message_response_serialzier = ChatMessageSerializer(old_messages, many=True)
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
    
    class _ChatResponseDto:
        def __init__(self, old_messages: list[dict], last_evaluated_key: dict):
            self.old_messages = old_messages
            self.last_evaluated_key = last_evaluated_key