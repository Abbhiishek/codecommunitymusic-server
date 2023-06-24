from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from app.Models.models import Forum
from app.serializers import ForumSerializer , UpdateForumserializer , Chatserializer
from app.libs.oauth2 import get_current_user


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def forum(request , slug=None):
    discussion_id = slug
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    if request.method == 'GET':
        if discussion_id:
            try:
                discussion = Forum.objects.get(slug=discussion_id)
                serializer = ForumSerializer(discussion)
                return JsonResponse({
                    "data": serializer.data,
                    "messsage": f'Forum found successfully with id {discussion_id}'
                }, status=status.HTTP_200_OK)
            except Forum.DoesNotExist:
                return JsonResponse({'message': f'Forum not found with the id {discussion_id}'}, status=status.HTTP_404_NOT_FOUND)

        else:
            discussions = Forum.objects.all().order_by('-created_at')
            serializer = ForumSerializer(discussions, many=True)
            return JsonResponse({
                    'data': serializer.data,
                    'message': 'Forum fetched successfully'
                }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        data['author'] = logged_in_user.username
        serializer = ForumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logged_in_user.karma += 100
            logged_in_user.save()
            return JsonResponse({
                "data": serializer.data,
                "message": "Forum created successfully"
            }, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # check if Discussions id is provided and the fecth the Discussionsa and check if the user is the author of the Discussions
        if discussion_id:
            try:
                discussion = Forum.objects.get(slug=discussion_id)
                print(discussion.author)
                print(logged_in_user.username)
                if discussion.author.username == logged_in_user.username:
                    serializer = UpdateForumserializer(
                        discussion, data=request.data , partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({
                            "data": serializer.data,
                            "message": f'Discussions updated successfully with id {discussion_id}'
                        }, status=status.HTTP_200_OK)
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse({'message': 'You are not authorized to update this Discussions'}, status=status.HTTP_401_UNAUTHORIZED)
            except Forum.DoesNotExist:
                return JsonResponse({'message': f'Discussions not found with the id {discussion_id}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'Please provide the Discussions id'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if discussion_id:
            try:
                discussion = Forum.objects.get(slug=discussion_id)
                if discussion.author.username == logged_in_user.username:
                    discussion.delete()
                    return JsonResponse({'message': f'Discussions deleted successfully with id {discussion_id}'
                                         }, status=status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({'message': 'You are not authorized to delete this Discussions'}, status=status.HTTP_401_UNAUTHORIZED)
            except Forum.DoesNotExist:
                return JsonResponse({'message': f'Discussions not found with the id {discussion_id}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'Please provide the Discussions id'}, status=status.HTTP_400_BAD_REQUEST)







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
        
