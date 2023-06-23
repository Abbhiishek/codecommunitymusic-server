from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User




class Todo(models.Model):
    author =  models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="todo_author")
    todo = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )