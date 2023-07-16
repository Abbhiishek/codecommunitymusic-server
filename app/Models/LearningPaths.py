from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User
from .Courses import Course

class LearningPath(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(User, related_name="authors" , blank=False)
    students = models.ManyToManyField(User, related_name="students" , blank=True)
    about = models.TextField( blank=True , default="Welome to new Track of Learning")
    level = models.TextField(max_length=200, blank=True , default="Beginner", choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ])
    slug = models.TextField(unique=True , primary_key=True)
    is_Active = models.BooleanField(default=True)
    courses = models.ManyToManyField(Course, related_name="courses" , blank=True)
    resources = ArrayField(models.TextField(blank=True), blank=True, default=list)


    def __str__(self):
        return self.title

