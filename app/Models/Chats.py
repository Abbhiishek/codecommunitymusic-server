from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User
from .Forums import Forum


class Chat(models.Model):
    """
    This class is used to create a chat model
    """
    id = models.AutoField(primary_key=True)
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="chat_author" )
    upvotes = models.ManyToManyField(User, related_name="chat_upvotes" , blank=True)
    reply = models.ManyToManyField(
        "self", related_name="comment_reply", symmetrical=False , blank=True)

    def __str__(self):
        return self.content