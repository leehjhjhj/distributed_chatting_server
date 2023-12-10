from members.models import Member
from members.serializers import RefreshAccessRequestSerialzier, RefreshAccessResponseSerialzier
from rest_framework_simplejwt.tokens import RefreshToken
from redis import Redis
from utils.redis_utils import get_redis_connection
from members.domains import MemberRepository
from utils.token import TokenValidator

class TokenService:
    def __init__(self, member_repository: MemberRepository, *args, **kwargs):
        self._member_repository = member_repository

    def refresh_access_token(self, request_data: dict):
        refresh_access_request_serializer = RefreshAccessRequestSerialzier(data=request_data)
        refresh_access_request_serializer.is_valid(raise_exception=True)
        refresh_data = refresh_access_request_serializer.validated_data

        refresh_token = refresh_data.get('refresh_token')
        refresh_token_user_id = TokenValidator.get_user_id_from_refresh_token(refresh_token)
        user_id: int = refresh_token_user_id
        member: Member = self._member_repository.find_member_by_id(user_id)

        token_validator = TokenValidator(token=refresh_token, user_id=member.id)
        token_validator.validate_token()
        token_validator.validate_already_logout()
        token_validator.validate_refresh_token_match()

        new_refresh: RefreshToken = RefreshToken.for_user(member)
        access_token = new_refresh.access_token

        redis_conn: Redis = get_redis_connection(db_select=3)
        redis_conn.set(member.id, str(new_refresh))

        refresh_access_response_serializer = RefreshAccessResponseSerialzier(self._TokenDto(access_token, new_refresh))
        return refresh_access_response_serializer.data
    
    class _TokenDto:
        def __init__(self, access_token: str, refresh_token: str):
            self.access_token = access_token
            self.refresh_token = refresh_token