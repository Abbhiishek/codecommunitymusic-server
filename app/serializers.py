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

class AllUserSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the user model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username' , 'display_name' , 'profile_pic' , 'created_at' , 'karma']

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



class ForumUserSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the forum model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username', 'display_name', 'profile_pic' , 'created_at' , 'karma']


class ForumSerializer(serializers.ModelSerializer):

    upvotes = ForumUserSerializer(many=True)
    author = ForumUserSerializer()
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
        serializer = ForumUserSerializer(author)
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



class LeaderboardSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the leaderboard model
    """
    class Meta:
        # specify the model to use
        model = User
        # specify the fields to be serialized
        fields = ['username', 'display_name', 'profile_pic' , 'created_at' , 'karma']




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
        serializer = ForumUserSerializer(author)
        return serializer.data
    def get_replies(self, comment):
        replies = comment.replies.all()
        serializer = CommentSerializer(replies, many=True)
        return serializer.data
    



class SubCourseSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the subcourse model
    """
    class Meta:
        # specify the model to use
        model = SubCourse
        # specify the fields to be serialized
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the course model
    """
    authors = ForumUserSerializer(many=True)
    sub_courses = SubCourseSerializer(many=True)
    students_count = serializers.SerializerMethodField()
    class Meta:
        # specify the model to use
        model = Course
        # specify the fields to be serialized
        fields = '__all__'

    def get_students_count(self, course):
        return course.students.count()



class AllLearningPathSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the learning path model
    """
    courses_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    class Meta:
        # specify the model to use
        model = LearningPath
        # specify the fields to be serialized
        fields = '__all__'

    def get_courses_count(self, learning_path):
        return learning_path.courses.count()
    
    def get_students_count(self, learning_path):
        return learning_path.students.count()

class LearningPathSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the learning path model
    """
    courses_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    ## order the courses by their order in the learning paths
    courses = serializers.SerializerMethodField()
    authors = ForumUserSerializer(many=True)
    students = ForumUserSerializer(many=True)
    class Meta:
        # specify the model to use
        model = LearningPath
        # specify the fields to be serialized
        fields = '__all__'
    
    def get_courses_count(self, learning_path):
        return learning_path.courses.count()
    
    def get_students_count(self, learning_path):
        return learning_path.students.count()
    
    def get_courses(self, learning_path):
        courses = learning_path.courses.all().order_by('-created_at')
        serializer = CourseSerializer(courses, many=True)
        return serializer.data




class AllCourseSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the course model
    """
    authors = ForumUserSerializer(many=True)
    students_count = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    class Meta:
        # specify the model to use
        model = Course
        # specify the fields to be serialized
        fields = '__all__'

    def get_sub_courses_count(self, course):
        return course.sub_courses.count()
    
    def get_students_count(self, course):
        return course.students.count()
    
    def get_lessons_count(self, course):
        return course.sub_courses.count()
    