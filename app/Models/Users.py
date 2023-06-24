
from django.db import models
from django.contrib.postgres.fields import ArrayField


gender_choices = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
    ("Prefer not to say", "Prefer not to say")
]


class User(models.Model):
    """
    This class is used to create a user model
    :param username: username of the user
    :param fullname: fullname of the user
    :param email: email of the user
    :param password: password of the user
    :param created_at: date and time when the user was created
    :param updated_at: date and time when the user was updated

    """
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    karma = models.IntegerField(default=0)
    email = models.EmailField(max_length=255, unique=True)
    skills = ArrayField(models.CharField(max_length=255),
                        default=list, size=15, blank=True)
    interests = ArrayField(models.CharField(
        max_length=255), size=15, default=list, blank=True)
    gender = models.CharField(
        max_length=255, default="Prefer not to say", choices=gender_choices
    )
    age = models.IntegerField(default=18)
    phone = models.BigIntegerField(default=0)
    bio = models.TextField(default="I am a new user", auto_created=True)
    profile_pic = models.TextField(
        default="https://img.freepik.com/premium-vector/anime-guy-beach_24911-70757.jpg")
    banner_pic = models.TextField(
        default="https://img.freepik.com/free-photo/psychedelic-paper-shapes-with-copy-space_23-2149378246.jpg?w=1800&t=st=1685775473~exp=1685776073~hmac=5f072e26cc9a086a94fa84df41dd56e01ba69cdcbf9efd71891a81e6a9059a11")

    followers = models.ManyToManyField(
        "self", blank=True , related_name="followers" )
    following = models.ManyToManyField(
        "self", blank=True , related_name="following")
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    password = models.TextField(max_length=255)
    github = models.TextField( null=True, blank=True)
    linkedin = models.TextField( null=True, blank=True)
    twitter = models.TextField(null=True, blank=True)
    website = models.TextField( null=True, blank=True)
    profession = models.TextField( null=True, blank=True)
    location = models.TextField( null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    temp_otp = models.IntegerField(default=0, null=True, blank=True)
    temp_otp_time = models.DateTimeField(null=True, blank=True)
    reset_password_token = models.CharField(
        max_length=255, null=True, blank=True)
    reset_password_token_time = models.DateTimeField(null=True, blank=True)
    account_setup_completed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.username
