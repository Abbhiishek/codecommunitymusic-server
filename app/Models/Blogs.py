from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    replyto = models.ForeignKey("self", on_delete=models.SET_NULL ,  null=True , related_name="reply_to")
    replies = models.ManyToManyField("self", related_name="replies", blank=True)


class Blog(models.Model):
    title =  models.CharField(max_length=255)
    ## json field
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    appreciate = models.ManyToManyField(User, related_name="appreciate", blank=True)
    tags = ArrayField(models.CharField(max_length=255), size=15, default=list, blank=True)
    is_published = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    comment = models.ManyToManyField(Comment, related_name="comment", blank=True)



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    # Add other fields for the Vote model




