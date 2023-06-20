from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from app.Models.models import User
from django.core.cache import cache

from app.serializers import LeaderboardSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



@api_view(['GET'])
def leaderboard(request):
    leaderboard = cache.get('leaderboard')
    if leaderboard is None:
        leaderboard = User.objects.order_by('-karma')[:100]
        cache.set('leaderboard', leaderboard, timeout=60*60)
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return JsonResponse({
            'leaderboard': serializer.data
        })
    else:
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return JsonResponse({
            'leaderboard': serializer.data
        })