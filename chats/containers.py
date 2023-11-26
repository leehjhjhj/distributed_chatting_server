from dependency_injector import containers, providers
from chats.domains import ChatRepository
from chats.applications import ChatService, ChatGetService

class ChatsContainer(containers.DeclarativeContainer):
    chat_repository=providers.Factory(ChatRepository)
    chat_service=providers.Factory(
        ChatService,
        chat_repository=chat_repository
    )
    chat_get_service = providers.Factory(
        ChatGetService,
        chat_repository
    )
