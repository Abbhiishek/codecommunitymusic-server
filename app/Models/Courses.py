

from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User





class SubCourse(models.Model):
    title=  models.TextField()
    description = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    about= models.TextField(max_length=200, blank=True , default="Welome to new SubCourse of Learning")
    is_Active= models.BooleanField(default=True)


class Course(models.Model):
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(User, related_name="course_authors" , blank=False)
    students = models.ManyToManyField(User, related_name="course_students" , blank=True)
    about = models.TextField( blank=True , default="Welome to new Course of Learning")
    slug = models.TextField(unique=True , primary_key=True)
    is_Active = models.BooleanField(default=True)
    sub_courses = models.ManyToManyField(SubCourse, related_name="sub_courses" , blank=True)
    resources = ArrayField(models.TextField(blank=True), blank=True, default=list)


    def __str__(self):
        return self.title