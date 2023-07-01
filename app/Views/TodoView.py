from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from app.Models.models import Todo
from app.serializers import TodoSerializer , UpdateTodoSerializer
from app.libs.oauth2 import get_current_user
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET' , 'POST'])
def gettodo(request , username=None):
    if request.method == 'GET':
        if username:
            try:
                cached_todo = cache.get(f"todo {username}")
                if cached_todo is not None:
                    return JsonResponse({
                        'data': cached_todo,
                        'message': f'Todo found successfully with for the user {username}'
                    }, status=status.HTTP_200_OK)
                todo = Todo.objects.filter(author__username=username).order_by('-created_at')
                serializer = TodoSerializer(todo, many=True)
                cache.set(f"todo {username}", serializer.data, timeout=CACHE_TTL)
                return JsonResponse({
                    "data": serializer.data,
                    "messsage": f'Todo found successfully with for the user {username}'
                }, status=status.HTTP_200_OK)
            except Todo.DoesNotExist:
                return JsonResponse({'message': f'Todo not found with the id {username}'}, status=status.HTTP_404_NOT_FOUND)

        else:
            todos = Todo.objects.all()
            serializer = TodoSerializer(todos, many=True)
            return JsonResponse({
                    'data': serializer.data,
                    'message': 'Todo fetched successfully'
                }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        data = request.data
        data['author'] = username
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            todo = Todo.objects.filter(author__username=username).order_by('-created_at')
            serializer = TodoSerializer(todo, many=True)
            cache.set(f"todo {username}", serializer.data, timeout=CACHE_TTL)
            return JsonResponse({
                "data": serializer.data,
                "message": "Todo created successfully"
            }, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
def updatetodo(request, username=None,  todo_id=None):
    try:
        todo = Todo.objects.get(
            Q(id=todo_id) & Q(author=username)
        )
    except Todo.DoesNotExist:
        return JsonResponse({'message': f'Todo not found with the id {todo_id}'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    serializer = UpdateTodoSerializer(todo, data=data , partial=True)
    if serializer.is_valid():
        serializer.save()
        todo = Todo.objects.filter(author__username=username).order_by('-created_at')
        serializer = TodoSerializer(todo, many=True)
        cache.set(f"todo {username}", serializer.data, timeout=CACHE_TTL)
        return JsonResponse({
            "data": serializer.data,
            "message": "Todo updated successfully"
        }, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deletetodo(request, username=None, todo_id=None):
    try:
        todo = Todo.objects.get(
            Q(id=todo_id) & Q(author__username=username)
        )
    except Todo.DoesNotExist:
        return JsonResponse({'message': f'Todo not found with the id {todo_id}'}, status=status.HTTP_404_NOT_FOUND)

    todo.delete()
    todo = Todo.objects.filter(author__username=username).order_by('-created_at')
    serializer = TodoSerializer(todo, many=True)
    cache.set(f"todo {username}", serializer.data, timeout=CACHE_TTL)
    return JsonResponse({'message': 'Todo deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

