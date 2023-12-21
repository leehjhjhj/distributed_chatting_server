from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from chats.containers import ChatsContainer
from rest_framework.permissions import IsAuthenticated

class ChatDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chat_service = ChatsContainer.chat_service()

    def delete(self, request, chat_id: int):
        self._chat_service.delete_chat(chat_id, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)