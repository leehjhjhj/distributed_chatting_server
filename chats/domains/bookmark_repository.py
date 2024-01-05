from chats.domains import Bookmark, Chat
from django.shortcuts import get_object_or_404

class BookmarkRepository:

    def save_bookmark(self, bookmark: Bookmark):
        bookmark.save()

    def find_bookmark_by_member_and_chat(self, member, chat: Chat):
        return Bookmark.objects.filter(member=member, chat=chat).first()
    
    def delete_bookmark(self, bookmark: Bookmark):
        bookmark.delete()