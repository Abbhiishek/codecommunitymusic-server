from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from  datetime import datetime


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# end point to list all the users /allusers


routes = {
    "routes": {
        '/': 'GET',
        '/allusers': 'GET',
        '/getuser': 'GET',
        '/login': 'POST',
    }
}


@api_view(['GET'])
def getallavailableroutes(request):
    starttime = datetime.now()
    print("getallavailableroutes fetching from cache")
    list = cache.get('getallavailableroutes')
    if list is None:
        if request.method == 'GET':
            cache.set('getallavailableroutes', routes, timeout=60*1500)
            endtime = datetime.now()
            return JsonResponse({
            "message": "success",
            "time_taken": str(endtime - starttime),
            "server": "db",
            "data": routes,
        }, status=status.HTTP_200_OK)
    else:
        endtime = datetime.now()
        return JsonResponse({
            "message": "success",
            "time_taken": str(endtime - starttime),
            "data": list,
            "server": "cache server v2"
        }, status=status.HTTP_200_OK)
    
