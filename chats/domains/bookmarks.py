from django.db import models

class Bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey('members.Member', models.DO_NOTHING, related_name='bookmarks')
    chat = models.ForeignKey('Chat', models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmarks'