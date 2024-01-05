from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from chats.containers import ChatsContainer
from rest_framework.permissions import IsAuthenticated

class BookmarkView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bookmark_service = ChatsContainer.bookmark_service()

    def post(self, request):
        self._bookmark_service.create_delete_bookmark(request.data, request.user)
        return Response(status=status.HTTP_200_OK)