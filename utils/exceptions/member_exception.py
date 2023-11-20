from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework import status
from django.core.exceptions import ValidationError

class PasswordWrongError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '비밀번호가 틀렸습니다. 다시 확인해주세요.'