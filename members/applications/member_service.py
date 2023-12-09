from members.domains import MemberRepository
from members.serializers import (
                            SignupRequestSerializer,
                            SigninRequestSerialzier,
                            SigninResponseSerializer,
                            LogoutRequestSerializer,
                        )
from members.domains import Member
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from utils.exceptions import PasswordWrongError
from utils.token import TokenValidator
from utils.redis_utils import get_redis_connection
from redis import Redis

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

        redis_conn: Redis = get_redis_connection(db_select=3)
        redis_conn.set(member.id, str(refresh))

        signin_serializer = SigninResponseSerializer(self.SigninDto(access_token, refresh, member))
        return signin_serializer.data
    
    def logout(self, request_data: dict):
        logout_request_serialzier = LogoutRequestSerializer(data=request_data)
        logout_request_serialzier.is_valid(raise_exception=True)
        logout_data: dict = logout_request_serialzier.validated_data
        
        refresh_token = logout_data.get('refresh_token')
        user_id = TokenValidator.get_user_id_from_refresh_token(refresh_token)
        redis_conn: Redis = get_redis_connection(db_select=3)
        redis_conn.delete(user_id)

    class SigninDto:
        def __init__(self, access_token: str, refresh_token: str, member: Member):
            self.access_token = access_token
            self.refresh_token = refresh_token
            self.member = member