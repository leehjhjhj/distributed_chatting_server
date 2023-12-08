from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from utils.redis_utils import get_redis_connection
from django.core.exceptions import ValidationError
from redis import Redis

def validate_token(token: str):
    try:
        RefreshToken(token)
    except (InvalidToken, TokenError):
        raise ValidationError('유효한 토큰이 아닙니다.')

def validate_user(token: str, user_id: int):
    token_object = RefreshToken(token)
    token_user_id: int = token_object.payload.get('user_id')
    if token_user_id != user_id:
        raise ValidationError('로그인한 유저와 토큰의 정보가 다릅니다.')

def validate_already_logout(user_id: int):
    redis_conn: Redis = get_redis_connection(db=3)
    user_id = str(user_id)

    if not redis_conn.exists(user_id):
        raise ValidationError("로그아웃 한 유저입니다.")