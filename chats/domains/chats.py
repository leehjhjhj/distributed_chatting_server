from django.db import models
from members.domains import Member

class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=64)
    made_by = models.ForeignKey('members.Member', models.DO_NOTHING)
    max_capacity = models.IntegerField()
    headcount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def chat_group_name(self):
        return self.make_call_group_name(call=self)

    @staticmethod
    def make_chat_group_name(chat_id=None):
        return f"chat-{chat_id}"