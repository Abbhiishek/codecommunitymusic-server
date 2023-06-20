
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from app.Models.models import Chat
from app.serializers import Chatserializer , UpdateChatserializer
from app.libs.oauth2 import get_current_user


@api_view(['GET', 'POST'])
def chat(request , forum_slug=None , chat_id=None):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    if request.method == 'GET':
        if forum_slug:
            try:
                chat = Chat.objects.filter(forum__slug=forum_slug).order_by('-created_at')
                serializer = Chatserializer(chat, many=True)
                return JsonResponse({
                    "data": serializer.data,
                    "messsage": f'Chat found successfully with for the forum {forum_slug}'
                }, status=status.HTTP_200_OK)
            except Chat.DoesNotExist:
                return JsonResponse({'message': f'Chat not found with the id {chat_id}'}, status=status.HTTP_404_NOT_FOUND)

        else:
            chats = Chat.objects.all()
            serializer = Chatserializer(chats, many=True)
            return JsonResponse({
                    'data': serializer.data,
                    'message': 'Chat fetched successfully'
                }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        data['author'] = logged_in_user.username
        data['forum'] = forum_slug
        serializer = Chatserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "data": serializer.data,
                "message": "Chat created successfully"
            }, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)