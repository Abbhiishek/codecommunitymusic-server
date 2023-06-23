from rest_framework import serializers
from rest_framework.response import Response

from .Models.models import *


class UserSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the user model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = '__all__'
        # specify the extra keyword arguments such as read_only_fields\
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.ModelSerializer):
    """

    This class is used to serialize the signup model 

    """

    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['email', 'username', 'password']
        # specify the extra keyword arguments such as read_only_fields
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ProjectSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the project model
    """
    class Meta:
        # specify the model to use
        model = Projects
        # specify the fields to be serialized
        fields = '__all__'


class UpdateProjectSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the project model
    """
    class Meta:
        # specify the model to use
        model = Projects
        # specify the fields to be serialized
        exclude = ['author', 'id', 'upvotes', 'downvotes', 'comments']


class ForumSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the discussion model
    """
    class Meta:
        # specify the model to use
        model = Forum
        # specify the fields to be serialized
        fields = '__all__'


class UpdateForumserializer(serializers.ModelSerializer):
    """
    This class is used to serialize the discussion model
    """
    class Meta:
        # specify the model to use
        model = Forum
        # specify the fields to be serialized
        exclude = ['author', ]



class LeaderboardSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the leaderboard model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username', 'display_name', 'profile_pic' , 'created_at' , 'karma']



class Chatserializer(serializers.ModelSerializer):
    """
    This class is used to serialize the chat model
    """
    class Meta:
        # specify the model to use
        model = Chat
        # specify the fields to be serialized
        fields = '__all__'


class UpdateChatserializer(serializers.ModelSerializer):
    """
    This class is used to serialize the chat model
    """
    class Meta:
        # specify the model to use
        model = Chat
        # specify the fields to be serialized
        exclude = ['author', 'id', 'upvotes', 'downvotes', 'comments']



class TodoSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the todo model
    """
    class Meta:
        # specify the model to use
        model = Todo
        # specify the fields to be serialized
        fields = '__all__'

class UpdateTodoSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the todo model
    """
    class Meta:
        # specify the model to use
        model = Todo
        # specify the fields to be serialized
        exclude = ['author']