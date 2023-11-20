from rest_framework import serializers
from members.domains import Member
from django.contrib.auth.hashers import make_password

class SignupRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = ('email', 'password', 'nickname')

    def validate_password(self, value):
        return make_password(value)