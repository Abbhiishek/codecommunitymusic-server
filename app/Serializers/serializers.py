from rest_framework import serializers
from app.Models.models import *



class ShortUserSerializer(serializers.ModelSerializer):
    """
    schema model for displaying user data in short form 

    username \n
    diaplay_name \n
    profile_pic \n
    created_at \n
    karma : number

    """
    class Meta:
        model = User
        fields = ['username', 'display_name', 'profile_pic' , 'created_at' , 'karma']



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


class LeaderboardSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the leaderboard model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username', 'display_name', 'profile_pic' , 'created_at' , 'karma']
