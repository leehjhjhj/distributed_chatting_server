from rest_framework import serializers
from chats.domains import Chat

class ChatCreateRequestSerializer(serializers.ModelSerializer):
    maxCapacity = serializers.CharField(source='max_capacity')
    
    class Meta:
        model = Chat
        fields = ('name', 'description', 'maxCapacity')