from rest_framework import serializers
from members.domains import Member
from django.contrib.auth.hashers import make_password
from utils.validators import validate_password, validate_email, validate_nickname

class SignupRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(validators=[validate_password])
    nickname = serializers.CharField(validators=[validate_nickname])
    class Meta:
        model = Member
        fields = ('email', 'password', 'nickname')

    def validate_password(self, value):
        return make_password(value)
    
class SigninRequestSerialzier(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = Member
        fields = ('email', 'password')

class MemberResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = ('id', 'email', 'nickname')

class SigninResponseSerializer(serializers.Serializer):
    accessToken = serializers.CharField(source='access_token')
    refreshToken = serializers.CharField(source='refresh_token')
    member = MemberResponseSerializer()

class LogoutRequestSerializer(serializers.Serializer):
    userId = serializers.IntegerField(source='user_id')

class RefreshAccessRequestSerialzier(serializers.Serializer):
    refreshToken = serializers.CharField(source='refresh_token')

class RefreshAccessResponseSerialzier(serializers.Serializer):
    accessToken = serializers.CharField(source='access_token')
    refreshToken = serializers.CharField(source='refresh_token')