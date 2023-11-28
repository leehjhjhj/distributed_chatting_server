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
    chatTime = serializers.CharField(source='chat_time')

class LastEvaluatedKeySerailzier(serializers.Serializer):
    chatId = serializers.CharField(source='chat_id')
    timestamp = serializers.DateTimeField()

class ChatJoinResponseSerializer(serializers.Serializer):
    joinedMembers = serializers.ListField(child=serializers.CharField(), source='joined_members')
    lastEvaluatedKey = LastEvaluatedKeySerailzier(source='last_evaluated_key')
    oldmessages = ChatMessageSerializer(source='old_messages', many=True)

class ChatMessageResponseSerializer(serializers.Serializer):
    lastEvaluatedKey = LastEvaluatedKeySerailzier(source='last_evaluated_key')
    oldMessages = ChatMessageSerializer(source='old_messages', many=True)

class ChatObjectResponseSerailzier(serializers.ModelSerializer):
    madeBy = serializers.CharField(source='made_by.nickname')
    maxCapacity = serializers.IntegerField(source='max_capacity')

    class Meta:
        model = Chat
        fields = ('id', 'name', 'description', 'madeBy', 'maxCapacity',)

class JoinedMembersResponseSerializer(serializers.Serializer):
    joinedMembers = serializers.ListField(child=serializers.CharField(), source='joined_members')