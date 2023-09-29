from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from app.Serializers.LearningPathSerializer import *
from app.Models.models import *
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@api_view(['GET'])
def get_all_learning_paths(request):
    try:
        cached_learningpaths = cache.get('learningpaths')
        if cached_learningpaths is None:
            learning_paths = LearningPath.objects.filter(is_Active=True).order_by('-title' , '-created_at')
            serializer = AllLearningPathSerializer(learning_paths, many=True)
            cache.set('learningpaths', serializer.data , timeout=CACHE_TTL)
            return JsonResponse({
                "learning_paths": serializer.data
            }, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                "learning_paths": cached_learningpaths
            }, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['GET'])
def get_learning_path(request, slug):
    try:
        cached_learningpath = cache.get('learningpath' + slug)
        if cached_learningpath is None:
            learning_path = LearningPath.objects.get(slug=slug , is_Active=True)
            serializer = LearningPathSerializer(learning_path)
            cache.set('learningpath' + slug, serializer.data , timeout=0)
            return JsonResponse({
                "learning_path": serializer.data
            }, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                "learning_path": cached_learningpath
            }, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({"error": str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)