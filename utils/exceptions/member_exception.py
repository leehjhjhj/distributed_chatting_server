from rest_framework.exceptions import APIException
from rest_framework import status

class PasswordWrongError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '비밀번호가 틀렸습니다. 다시 확인해주세요.'

class RequiredLoginError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '로그인이 필요합니다.'