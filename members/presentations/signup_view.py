from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from members.containers import MembersContainer

class SignUpView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._members_service = MembersContainer.member_service()

    def post(self, request):
        self._members_service.signup(request.data)
        return Response(status=status.HTTP_201_CREATED)