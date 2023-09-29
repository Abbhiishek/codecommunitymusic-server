from rest_framework import serializers
from app.Models.models import *
from app.Serializers.serializers import *


class ForumSerializer(serializers.ModelSerializer):

    upvotes = ShortUserSerializer(many=True)
    author = ShortUserSerializer()
    class Meta:
        # specify the model to use
        model = Forum
        # specify the fields to be serialized
        fields = '__all__'


class CreateForumSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the forum model
    """
    class Meta:
        # specify the model to use
        model = Forum
        # specify the fields to be serialized
        fields = '__all__'




class ChatSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all(), required=False)
    replies = serializers.SerializerMethodField()
    class Meta:

        model = Chat
        fields = [ "id", 'content', 'created_at', 'updated_at', 'author', 'reply_to', 'replies']

    def get_author(self, chat):
        author = chat.author
        serializer = ShortUserSerializer(author)
        return serializer.data

    def get_replies(self, chat):
        replies = chat.replies.all()
        serializer = ChatSerializer(replies, many=True)
        return serializer.data
    
    
    
class CreateChatSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the chat model
    """
    class Meta:
        # specify the model to use
        model = Chat
        # specify the fields to be serialized
        fields = '__all__'

class UpdateForumSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the discussion model
    """
    class Meta:
        # specify the model to use
        model = Forum
        # specify the fields to be serialized
        exclude = ['author', 'slug']
