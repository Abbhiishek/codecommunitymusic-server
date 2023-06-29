from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    appreciators = models.ManyToManyField(User, related_name='appreciated_blogs' , blank=True)
    tags = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    is_published = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)



class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')