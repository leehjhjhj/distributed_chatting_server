from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from chats.containers import ChatsContainer
from rest_framework.permissions import IsAuthenticated

class ChatGetMoreMessageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chat_service = ChatsContainer.chat_service()

    def get(self, request, chat_id: int):
        last_evaluated_key = request.query_params.get('key')
        response = self._chat_service.get_more_messages(chat_id, last_evaluated_key)
        return Response(response, status=status.HTTP_200_OK)