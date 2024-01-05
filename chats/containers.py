from dependency_injector import containers, providers
from chats.domains import ChatRepository, BookmarkRepository
from chats.applications import ChatService, ChatGetService, BookmarkService

class ChatsContainer(containers.DeclarativeContainer):
    chat_repository=providers.Factory(ChatRepository)
    bookmark_repository = providers.Factory(BookmarkRepository)
    chat_service=providers.Factory(
        ChatService,
        chat_repository=chat_repository
    )
    chat_get_service = providers.Factory(
        ChatGetService,
        chat_repository
    )
    bookmark_service = providers.Factory(
        BookmarkService,
        bookmark_repository=bookmark_repository,
        chat_repository=chat_repository
    )
