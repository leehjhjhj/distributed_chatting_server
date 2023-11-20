from django.db import models
from members.domains import Member

class Participant(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Member, models.DO_NOTHING)
    chat = models.ForeignKey('Chat', models.DO_NOTHING)
    participated_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'participants'