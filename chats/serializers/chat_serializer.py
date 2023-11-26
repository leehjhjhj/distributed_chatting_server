from rest_framework import serializers
from chats.domains import Chat

class ChatCreateRequestSerializer(serializers.ModelSerializer):
    maxCapacity = serializers.CharField(source='max_capacity')
    
    class Meta:
        model = Chat
        fields = ('name', 'description', 'maxCapacity')

class ChatMessageSerializer(serializers.Serializer):
    userId = serializers.CharField(source='user_id')
    userNickname = serializers.CharField(source='user_nickname')
    timestamp = serializers.DateTimeField()
    messageId = serializers.CharField(source='message_id')
    message = serializers.CharField()
    chatId = serializers.CharField(source='chat_id')

class LastEvaluatedKeySerailzier(serializers.Serializer):
    chatId = serializers.CharField(source='chat_id')
    timestamp = serializers.DateTimeField()

class ChatMessageResponseSerializer(serializers.Serializer):
    lastEvaluatedKey = LastEvaluatedKeySerailzier(source='last_evaluated_key')
    oldMessages = ChatMessageSerializer(source='old_messages', many=True)

class ChatObjectResponseSerailzier(serializers.ModelSerializer):
    madeBy = serializers.CharField(source='made_by')
    maxCapacity = serializers.CharField(source='max_capacity')

    class Meta:
        model = Chat
        fields = ('id', 'name', 'description', 'madeBy', 'maxCapacity',)