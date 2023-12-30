from rest_framework import serializers

class BookmarkCreateRequestSerializer(serializers.Serializer):
    chatId = serializers.IntegerField(source='chat_id')