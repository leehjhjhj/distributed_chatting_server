from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from chats.containers import ChatsContainer
from rest_framework_simplejwt.authentication import JWTAuthentication

class ChatRoomGetView(APIView):
    authentication_classes = [JWTAuthentication]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chat_get_service = ChatsContainer.chat_get_service()

    def get(self, request, *args, **kwargs):
        order_by = request.query_params.get('order', 'latest')
        response = self._chat_get_service.get_all_chat_rooms(order_by, request.user)
        return Response(response, status=status.HTTP_200_OK)