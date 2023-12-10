from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from members.containers import MembersContainer

class RefreshAccessTokenView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token_service = MembersContainer.token_service()

    def post(self, request, *args, **kwargs):
        response = self._token_service.refresh_access_token(request.data)
        return Response(response, status=status.HTTP_200_OK)
