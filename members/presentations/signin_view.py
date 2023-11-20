from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from members.containers import MembersContainer

class SigninView(TokenObtainPairView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    def post(self, request, *args, **kwargs):
        response = self._members_service.signin(request.data)
        return Response(response, status=status.HTTP_200_OK)
