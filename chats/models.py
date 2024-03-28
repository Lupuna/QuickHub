from django.db import models
from team import models as team_models


class Chat(models.Model):
    title = models.CharField(max_length=250)
    employees = models.ManyToManyField(team_models.Employee, related_name='chats')

    class Meta:
        ordering = ['title']


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    employee_id = models.ForeignKey(team_models.Employee, on_delete=models.CASCADE, related_name='messages')
    last_update = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    json_with_content = models.JSONField(blank=True, default=dict)
