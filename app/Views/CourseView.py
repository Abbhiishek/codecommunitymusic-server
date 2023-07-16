from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from app.serializers import *
from app.Models.models import *
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



@api_view(['GET'])
def get_all_Courses(request):
    try:
        cached_courses = cache.get('courses')
        if cached_courses is None:
            courses = Course.objects.filter(is_Active=True).order_by('-title' , '-created_at')
            serializer = AllCourseSerializer(courses, many=True)
            cache.set('courses', serializer.data , timeout=0)
            return JsonResponse({
                "courses": serializer.data
            }, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                "courses": cached_courses
            }, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_Course(request, slug):
    try:
        cached_course = cache.get("course"+slug)
        if cached_course is None:
            course = Course.objects.get(slug=slug , is_Active=True)
            serializer = CourseSerializer(course, many=False)
            cache.set("course"+slug, serializer.data , timeout=0)
            return JsonResponse({
                "course": serializer.data
            }, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                "course": cached_course
            }, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
