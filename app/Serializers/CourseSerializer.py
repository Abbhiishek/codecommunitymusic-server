from rest_framework import serializers
from app.Models.models import *
from app.Serializers.serializers import *


class AllCourseSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the course model
    """
    authors = ShortUserSerializer(many=True)
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
    authors = ShortUserSerializer(many=True)
    sub_courses = SubCourseSerializer(many=True)
    students_count = serializers.SerializerMethodField()
    class Meta:
        # specify the model to use
        model = Course
        # specify the fields to be serialized
        fields = '__all__'

    def get_students_count(self, course):
        return course.students.count()
    


