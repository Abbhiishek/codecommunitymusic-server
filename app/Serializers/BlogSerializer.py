from rest_framework import serializers
from app.Models.models import *
from app.Serializers.serializers import *




class BlogUserSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the blog model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username', 'display_name', 'profile_pic' , 'created_at' , 'karma']



class CreateBlogSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the blog model
    """
    class Meta:
        # specify the model to use
        model = Blog
        # specify the fields to be serialized
        fields = '__all__'

        
class BlogSerializer(serializers.ModelSerializer):
    author = BlogUserSerializer()
    appreciators = BlogUserSerializer(many=True)
    class Meta:
        model = Blog
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'updated_at', 'author', 'reply_to', 'replies']
    def get_author(self, chat):
        author = chat.author
        serializer = ShortUserSerializer(author)
        return serializer.data
    def get_replies(self, comment):
        replies = comment.replies.all()
        serializer = CommentSerializer(replies, many=True)
        return serializer.data
    