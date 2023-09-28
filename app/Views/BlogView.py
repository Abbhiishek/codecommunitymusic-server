from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import status
from app.Models.models import Blog , Comment
from app.serializers import BlogSerializer , CommentSerializer , CreateBlogSerializer
from app.libs.oauth2 import get_current_user

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
def get_blog(request, slug=None):
    if slug:
        cached_data = cache.get(slug)
        if cached_data is None:
            try:
                blog = Blog.objects.get(slug=slug , is_published=True)
                serializer = BlogSerializer(blog)
                comments = Comment.objects.filter(blog=blog , reply_to=None)
                comments_serializer = CommentSerializer(comments, many=True)
                data = {
                    'blog': serializer.data,
                    'comments': comments_serializer.data
                }
                cache.set(slug, data, timeout=0)
                return JsonResponse({
                    'data': data,
                    'message': f'Blog found successfully with slug {slug}',
                    'server': 'db'
                }, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return JsonResponse({'message': f'Blog not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({
                'data': cached_data,
                'message': f'Blog found successfully with slug {slug}',
                'server': 'cache server v2'
            }, status=status.HTTP_200_OK)
    else:
        cached_data = cache.get('allblogs')
        if cached_data is None:
            blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
            serializer = BlogSerializer(blogs, many=True)
            data = serializer.data
            cache.set('allblogs', data, timeout=100)
            return JsonResponse({
                'data': data,
                'message': 'Success',
                'server': 'db'
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'data': cached_data,
                'message': 'Success',
                'server': 'cache server v2'
            }, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def create_blog(request):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    data = request.data
    data['author'] = logged_in_user.username
    serializer = CreateBlogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logged_in_user.karma += 80
        logged_in_user.save()
        blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
        serializer = BlogSerializer(blogs, many=True)
        data = serializer.data
        cache.set('allblogs', data, timeout=100)
        return JsonResponse({
            "data": serializer.data,
            "message": "Blog created successfully"
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_blog(request, slug):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return JsonResponse({'message': f'Blog not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)

    if blog.author != logged_in_user.username:
        return JsonResponse({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    serializer = BlogSerializer(blog, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            "data": serializer.data,
            "message": "Blog updated successfully"
        }, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_blog(request, slug):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return JsonResponse({'message': f'Blog not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)

    if blog.author != logged_in_user.username:
        return JsonResponse({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

    blog.delete()
    logged_in_user.karma -= 10
    logged_in_user.save()
    return JsonResponse({'message': f'Blog deleted successfully with the slug {slug}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def listBlogOfUser(request, username):
    if username:
            try:
                blogs = Blog.objects.filter(author__username=username).order_by('-created_at')
                serializer = BlogSerializer(blogs, many=True)
                return JsonResponse({
                    'data': serializer.data,
                    'message': 'Forum fetched successfully'
                }, status=status.HTTP_200_OK)
            except Blog.DoesNotExist:
                return JsonResponse({'message': f'Forum not found in user  {username}'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'Please provide the user id'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create_comment(request, slug):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return JsonResponse({'message': f'Blog not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data['author'] = logged_in_user.username
    data['blog'] = blog.id
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logged_in_user.karma += 5
        logged_in_user.save()
        return JsonResponse({
            "data": serializer.data,
            "message": "Comment created successfully"
        }, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_comment(request, slug, comment_id):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return JsonResponse({'message': f'Blog not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'message': f'Comment not found with the id {comment_id}'}, status=status.HTTP_404_NOT_FOUND)

    if comment.author != logged_in_user.username:
        return JsonResponse({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    serializer = CommentSerializer(comment, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({
            "data": serializer.data,
            "message": "Comment updated successfully"
        }, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def delete_comment(request, slug, comment_id):
    token_type, token = request.headers['Authorization'].split(' ')
    logged_in_user = get_current_user(token)

    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return JsonResponse({'message': f'Blog not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'message': f'Comment not found with the id {comment_id}'}, status=status.HTTP_404_NOT_FOUND)

    if comment.author != logged_in_user.username:
        return JsonResponse({'message': 'You are not authorized to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

    comment.delete()
    return JsonResponse({'message': f'Comment deleted successfully with the id {comment_id}'}, status=status.HTTP_200_OK)




