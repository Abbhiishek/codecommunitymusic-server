from rest_framework import serializers
from app.Models.models import *




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



class AllUserSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the user model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username' , 'display_name' , 'profile_pic' , 'created_at' , 'karma']
