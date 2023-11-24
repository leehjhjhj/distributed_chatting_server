from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from chats.domains import Chat
import logging

class ChatConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = ""
    
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
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = Chat.make_chat_group_name(chat_id)

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
        self.send_json({
            "type": "chat.message",
            "message": message_dict["message"]
        })