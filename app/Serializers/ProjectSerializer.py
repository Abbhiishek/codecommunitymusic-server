from rest_framework import serializers
from app.Models.models import *
from app.Serializers.serializers import *


class ProjectSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the project model
    """
    class Meta:
        # specify the model to use
        model = Project
        # specify the fields to be serialized
        fields = '__all__'


class UpdateProjectSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the project model
    """
    class Meta:
        # specify the model to use
        model = Project
        # specify the fields to be serialized
        exclude = ['author', 'id', 'upvotes', 'downvotes', 'comments']
