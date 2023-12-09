from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from members.containers import MembersContainer

class LogoutView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    def post(self, request, *args, **kwargs):
        response = self._members_service.logout(request.data)
        return Response(response, status=status.HTTP_204_NO_CONTENT)