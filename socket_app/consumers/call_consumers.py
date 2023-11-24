from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from chats.domains import Chat
from datetime import datetime
from decouple import config
from utils.date import current_time
import boto3
import logging

AWS_ACCCESS_KEY=config('AWS_ACCCESS_KEY')
AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY')

class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = ""
        self.nickname = ""
        self.dynamodb = boto3.resource(
            'dynamodb', region_name='ap-northeast-2',
            aws_access_key_id=AWS_ACCCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        self.table = self.dynamodb.Table('clclcafe')

    def receive_json(self, content, **kwargs):
        _type = content["type"]
        _message = content["message"]
        
        if _type == "chat.message":
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": _message
                }
            )
        else:
            logging.ERROR("오류:",_type)

    def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = Chat.make_chat_group_name(self.chat_id)

        user = self.scope["user"]
        self.nickname = user.nickname

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )

    def chat_message(self, message_dict):
        chat_id = self.chat_id
        user = self.scope["user"]
        now = datetime.now().isoformat()

        self.table.put_item(
        Item={
            'message_id': f'{chat_id}-{now}',
            'chat_id': chat_id,
            'user_id': user.id,
            'user_nickname': user.nickname,
            'message': message_dict["message"],
            'timestamp': now
        }
    )
        self.send_json({
            "type": "chat.message",
            "message": message_dict["message"],
            "nickname": self.nickname,
            "time": current_time()
        })