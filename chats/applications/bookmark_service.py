from chats.domains import ChatRepository, BookmarkRepository, Chat, Bookmark
from chats.serializers import BookmarkCreateRequestSerializer

class BookmarkService:
    def __init__(self, bookmark_repository: BookmarkRepository, chat_repository: ChatRepository, *args, **kwargs):
        self._bookmark_repository = bookmark_repository
        self._chat_repository = chat_repository

    def create_delete_bookmark(self, request_data: dict, user_data: dict):
        bookmark_create_request_serialzier = BookmarkCreateRequestSerializer(data=request_data)
        bookmark_create_request_serialzier.is_valid(raise_exception=True)
        bookmark_data = bookmark_create_request_serialzier.validated_data

        chat_id = bookmark_data.get('chat_id')
        chat: Chat = self._chat_repository.find_chat_by_id(chat_id)
        bookmark: Bookmark = self._bookmark_repository.find_bookmark_by_member_and_chat(user_data, chat)
        if bookmark:
            self._bookmark_repository.delete_bookmark(bookmark)
        else:
            bookmark = Bookmark(member=user_data, chat=chat)
            self._bookmark_repository.save_bookmark(bookmark)