from members.domains import MemberRepository
from members.serializers import SignupRequestSerializer

class MemberService:
    def __init__(self, member_repository: MemberRepository, *args, **kwargs):
        self._member_repository = member_repository

    def signup(self, request_data: dict):
        signup_request_serializer = SignupRequestSerializer(data=request_data)
        signup_request_serializer.is_valid(raise_exception=True)
        signup_request_serializer.save()
        