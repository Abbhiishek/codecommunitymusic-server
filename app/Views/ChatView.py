from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from app.Models.models import Forum , Chat
from app.serializers import CreateChatSerializer
from app.libs.oauth2 import get_current_user

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT




@api_view(['POST'])
def postanswerforforum(request , slug ):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        forum = Forum.objects.get(slug=slug)
    except Forum.DoesNotExist:
        return JsonResponse({'message': f'Forum not found with the slug: {slug}'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data
    answerSerializer = CreateChatSerializer(data=data  , partial=True)
    if answerSerializer.is_valid():
        answerSerializer.save()
        logged_in_user.karma += 5
        logged_in_user.save()
        return JsonResponse({
            "data": answerSerializer.data,
            "message": "Answer posted successfully"
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(answerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteanswerforforum(request , slug , id):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        forum = Forum.objects.get(slug=slug)
    except Forum.DoesNotExist:
        return JsonResponse({'message': f'Forum not found with the slug: {slug}'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        answer = Chat.objects.get(id=id)
    except Chat.DoesNotExist:
        return JsonResponse({'message': f'Answer not found with the id: {id}'}, status=status.HTTP_404_NOT_FOUND)
    
    if answer.author.username == logged_in_user.username:
        answer.delete()
        logged_in_user.karma -= 5
        logged_in_user.save()
        return JsonResponse({
            "message": "Answer deleted successfully"
        }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            "message": "You are not authorized to delete this answer"
        }, status=status.HTTP_401_UNAUTHORIZED)
