from django.db import models
from django.contrib.postgres.fields import ArrayField
from .Users import User


class Projects(models.Model):
    """
    This class is used to create a project model
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255)
    tags = ArrayField(models.CharField(max_length=255),
                      size=15, default=list, blank=True)
    tech_stack = ArrayField(models.CharField(
        max_length=255), size=15, default=list, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="project_author")
    collaborators = models.ManyToManyField(
        User, related_name="project_collaborators", blank=True)
    upvotes = models.ManyToManyField(
        User, related_name="project_upvotes", blank=True)
    bookmarks = models.ManyToManyField(
        User, related_name="project_bookmark", blank=True)
    views = models.ManyToManyField(
        User, related_name="project_views", blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    bannerImage = models.CharField(
        blank=True, default="https://t4.ftcdn.net/jpg/03/02/74/89/360_F_302748918_Vs76DTDodjhhkYuCEFahu0LcoDZkBuaW.jpg")
    mainImage = models.CharField(
        blank=True, default="https://t4.ftcdn.net/jpg/03/02/74/89/360_F_302748918_Vs76DTDodjhhkYuCEFahu0LcoDZkBuaW.jpg")
    demoLink = models.URLField(max_length=200, blank=True)
    githubLink = models.URLField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.slug
