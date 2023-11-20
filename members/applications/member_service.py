from members.domains import MemberRepository
from members.serializers import (
                            SignupRequestSerializer,
                            SigninRequestSerialzier,
                            SigninResponseSerializer,
                        )
from members.domains import Member
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken, Token
from utils.exceptions import PasswordWrongError

class MemberService:
    def __init__(self, member_repository: MemberRepository, *args, **kwargs):
        self._member_repository = member_repository

    def signup(self, request_data: dict):
        signup_request_serializer = SignupRequestSerializer(data=request_data)
        signup_request_serializer.is_valid(raise_exception=True)
        signup_request_serializer.save()
    
    def signin(self, request_data: dict):
        signin_request_serializer = SigninRequestSerialzier(data=request_data)
        signin_request_serializer.is_valid(raise_exception=True)
        signin_data: dict = signin_request_serializer.validated_data

        email = signin_data.get('email')
        password = signin_data.get('password')
        member: Member = self._member_repository.find_member_by_email(email=email)

        if not check_password(password, member.password):
            raise PasswordWrongError

        refresh: RefreshToken = RefreshToken.for_user(member)
        access_token = refresh.access_token
        signin_serializer = SigninResponseSerializer({'access_token': access_token, 'member': member})
        return signin_serializer.data