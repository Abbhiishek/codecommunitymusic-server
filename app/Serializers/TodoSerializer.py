from rest_framework import serializers
from app.Models.models import *



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


