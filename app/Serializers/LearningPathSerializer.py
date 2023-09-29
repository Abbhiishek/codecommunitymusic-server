from rest_framework import serializers
from app.Models.models import *
from app.Serializers.serializers import *
from app.Serializers.CourseSerializer import *


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
    authors = ShortUserSerializer(many=True)
    students = ShortUserSerializer(many=True)
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