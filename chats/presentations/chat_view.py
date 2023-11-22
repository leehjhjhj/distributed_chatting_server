from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from chats.containers import ChatsContainer

class ChatView(APIView):
    authentication_classes = [JWTAuthentication]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chat_service = ChatsContainer.chat_service()

    def post(self, request):
        self._chat_service.create_chat(request.data, request.user)
        return Response(status=status.HTTP_201_CREATED)