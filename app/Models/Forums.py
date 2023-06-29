from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User

class Forum(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name="upvotes" , blank=True)
    tags = ArrayField(models.CharField(max_length=200), default=None, blank=True)
    type = models.TextField(max_length=200, blank=True , default="Discussion")
    slug = models.TextField(unique=True , primary_key=True)
    is_closed = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class Chat(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, related_name="chat_upvotes" , blank=True)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


    def __str__(self):
        return self.content
