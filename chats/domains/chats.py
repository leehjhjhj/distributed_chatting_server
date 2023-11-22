from django.db import models
from members.domains import Member

class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=64)
    made_by = models.ForeignKey(Member, models.DO_NOTHING)
    max_capacity = models.IntegerField()
    headcount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    