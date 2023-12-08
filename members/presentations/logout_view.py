from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from members.containers import MembersContainer
from rest_framework_simplejwt.authentication import JWTAuthentication

class LogoutView(TokenObtainPairView):
    authentication_classes = [JWTAuthentication]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    def post(self, request, *args, **kwargs):
        response = self._members_service.logout(request.data, request.user)
        return Response(response, status=status.HTTP_204_NO_CONTENT)
