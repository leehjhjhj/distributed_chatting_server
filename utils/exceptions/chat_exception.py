from rest_framework.exceptions import APIException
from rest_framework import status

class OverMaxCountError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '채팅방이 꽉 찼습니다.'

class NoRightToDeleteChat(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '채팅창을 삭제할 권한이 없습니다.'