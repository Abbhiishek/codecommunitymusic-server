from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from app.Models.models import Forum , Chat
from app.Serializers.ForumSerializer import ForumSerializer , UpdateForumSerializer , ChatSerializer , CreateForumSerializer
from app.libs.oauth2 import get_current_user
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@api_view(['GET'])
def fetch_all_forums(request):
    cached_forums = cache.get('all_forums')
    if cached_forums is  None:
        forums = Forum.objects.all().order_by('-created_at')
        serializer = ForumSerializer(forums, many=True)
        cache.set('all_forums', serializer.data, timeout=CACHE_TTL)
        return JsonResponse({
            'data': serializer.data,
            'message': 'Forums fetched successfully'
        }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            'data': cached_forums,
            'message': 'Forums fetched successfully'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def fetch_forum(request, slug):
    try:
        forum = Forum.objects.get(slug=slug)
        serializer = ForumSerializer(forum)
        chats = Chat.objects.filter(forum=forum , reply_to=None)
        chats_serializer = ChatSerializer(chats, many=True)
        cache.set(f"forum {slug}", serializer.data, timeout=CACHE_TTL)
        cache.set(f"forum {slug} chats", chats_serializer.data, timeout=CACHE_TTL)
        return JsonResponse({
            "data": serializer.data,
            "comments": chats_serializer.data,
            "message": f'Forum found successfully with id {slug}'
        }, status=status.HTTP_200_OK)
    except Forum.DoesNotExist:
        return JsonResponse({'message': f'Forum not found with the id {slug}'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_forum(request):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    data = request.data
    data['author'] = logged_in_user.username
    serializer = CreateForumSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logged_in_user.karma += 10
        logged_in_user.save()
        new_All_Forums = Forum.objects.all().order_by('-created_at')
        serializer = ForumSerializer(new_All_Forums, many=True)
        cache.set('all_forums', serializer.data, timeout=CACHE_TTL)
        return JsonResponse({
            "data": serializer.data,
            "message": "Forum created successfully"
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_forum(request, slug):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        discussion = Forum.objects.get(slug=slug)
        if discussion.author.username == logged_in_user.username:
            serializer = UpdateForumSerializer(discussion, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                new_All_Forums = Forum.objects.all().order_by('-created_at')
                serializer = ForumSerializer(new_All_Forums, many=True)
                cache.set('all_forums', serializer.data, timeout=CACHE_TTL)
                new_forum = Forum.objects.get(slug=slug)
                serializer = ForumSerializer(new_forum)
                cache.set(f"forum {slug}", serializer.data, timeout=CACHE_TTL)
                return JsonResponse({
                    "data": serializer.data,
                    "message": f'Forum updated successfully with id {slug}'
                }, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'You are not authorized to update this Forum'}, status=status.HTTP_401_UNAUTHORIZED)
    except Forum.DoesNotExist:
        return JsonResponse({'message': f'Forum not found with the id {slug}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_forum(request, slug):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        discussion = Forum.objects.get(slug=slug)
        if discussion.author.username == logged_in_user.username:
            discussion.delete()
            new_All_Forums = Forum.objects.all().order_by('-created_at')
            serializer = ForumSerializer(new_All_Forums, many=True)
            cache.set('all_forums', serializer.data, timeout=CACHE_TTL)
            return JsonResponse({'message': f'Forum deleted successfully with id {slug}'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'message': 'You are not authorized to delete this Forum'}, status=status.HTTP_401_UNAUTHORIZED)
    except Forum.DoesNotExist:
        return JsonResponse({'message': f'Forum not found with the id {slug}'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def listForumOfUser(request , username=None):
    if request.method == 'GET':
        if username:
            try:
                discussions = Forum.objects.filter(author__username=username).order_by('-created_at')
                serializer = ForumSerializer(discussions, many=True)
                return JsonResponse({
                    'data': serializer.data,
                    'message': 'Forum fetched successfully'
                }, status=status.HTTP_200_OK)
            except Forum.DoesNotExist:
                return JsonResponse({'message': f'Forum not found in user  {username}'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return JsonResponse({'message': 'Please provide the Discussions id'}, status=status.HTTP_400_BAD_REQUEST)
        
