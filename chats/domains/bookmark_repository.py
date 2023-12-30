from chats.domains import Bookmark

class BookmarkRepository:

    def save_bookmark(self, bookmark: Bookmark):
        bookmark.save()