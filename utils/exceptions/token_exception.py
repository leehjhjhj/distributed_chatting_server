from rest_framework.exceptions import APIException
from rest_framework import status

class NotValidTokenError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유효한 리프레시 토큰이 아닙니다.'

class NotMatchTokenUserError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '로그인한 유저와 리프레시 토큰의 정보가 다릅니다.'

class AleadyLogoutUserError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 로그아웃 한 유저입니다.'

class RefreshTokenNotMatchError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '리프레시 토큰이 일치하지 않습니다.'