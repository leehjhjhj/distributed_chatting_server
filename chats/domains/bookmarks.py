from django.db import models

class Bookmark(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey('members.Member', models.DO_NOTHING)
    chat = models.ForeignKey('Chat', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmarks'