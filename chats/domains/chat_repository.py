from chats.domains import Chat

class ChatRepository:
    def save_chat(self, chat: Chat):
        chat.save()