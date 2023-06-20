from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User

class Forum(models.Model):
    """
    This class is used to create a discussion model
    :param title: title of the discussion
    :param description: description of the discussion
    :param created_at: date and time when the discussion was created
    :param updated_at: date and time when the discussion was updated
    :param user: user who created the discussion

    """
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    upvotes = models.ManyToManyField(
        User, related_name="upvotes", default=None, blank=True)
    tags = ArrayField(models.CharField(max_length=200), default=None, blank=True)
    type = models.CharField(max_length=200, blank=True , default="Discussion")
    slug = models.CharField( default=None, blank=True, unique=True , primary_key=True)
    is_closed = models.BooleanField(default=False)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
