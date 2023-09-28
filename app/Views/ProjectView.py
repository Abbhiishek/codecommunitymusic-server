from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from app.Models.models import Projects
from app.serializers import *
from app.libs.oauth2 import get_current_user
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
def allprojects(request, slug=None):
    cached_projects = cache.get('allprojects')
    if cached_projects is None:
        projects = Projects.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        cache.set('allprojects', serializer.data, timeout=200)
        return JsonResponse({
            "data": serializer.data,
            "message": "success",
            "server": "db"
        }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            "data": cached_projects,
            "message": "success",
            "server": "cache server v2"
        }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def project(request, slug=None):
    if request.method == 'GET':
        if slug:
            try:
                cached_project = cache.get("project-"+slug)
                if cached_project is None:
                    project = Projects.objects.get(slug=slug)
                    serializer = ProjectSerializer(project)
                    cache.set("project-"+slug, serializer.data, timeout=100)
                    return JsonResponse({
                        "data": serializer.data,
                        "messsage": f'Project found successfully with slug {slug}',
                        "server": "db"
                    }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({
                        "data": cached_project,
                        "messsage": f'Project found successfully with slug {slug}',
                        "server": "cache server v2"
                    }, status=status.HTTP_200_OK)
            except Projects.DoesNotExist:
                return JsonResponse({'message': f'Project not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)
        else:  # if the project id is not provided
            cached_projects = cache.get('allprojects')
            if cached_projects is None:
                projects = Projects.objects.all()
                serializer = ProjectSerializer(projects, many=True)
                cache.set('allprojects', serializer.data, timeout=0)
                return JsonResponse({
                    "data": serializer.data,
                    "message": "success",
                    "server": "db"
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({
                    "data": cached_projects,
                    "message": "success",
                    "server": "cache server v2"
                }, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        token_type, token = request.headers['Authorization'].split(' ')
        logged_in_user = get_current_user(token)
        data = request.data
        data['author'] = logged_in_user.username
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logged_in_user.karma += 80
            logged_in_user.save()
            projects = Projects.objects.filter(is_published=True).order_by('-created_at')
            serializer = ProjectSerializer(projects, many=True)
            cache.set('allprojects', serializer.data, timeout=100)
            return JsonResponse({
                "status": "success",
                "data": serializer.data,
                "message": "Project created successfully"
            }, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        token_type, token = request.headers['Authorization'].split(' ')
        logged_in_user = get_current_user(token)
        # check if project id is provided and the fecth the projecta and check if the user is the author of the project
        if slug:
            try:
                project = Projects.objects.get(id=slug)
                print(project.author)
                print(logged_in_user.username)
                if project.author.username == logged_in_user.username:
                    serializer = UpdateProjectSerializer(
                        project, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({
                            "data": serializer.data,
                            "message": f'Project updated successfully with slug {slug}'
                        }, status=status.HTTP_200_OK)
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse({'message': 'You are not authorized to update this project'}, status=status.HTTP_401_UNAUTHORIZED)
            except Projects.DoesNotExist:
                return JsonResponse({'message': f'Project not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'Please provide the project slug'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        token_type, token = request.headers['Authorization'].split(' ')
        logged_in_user = get_current_user(token)
        if slug:
            try:
                project = Projects.objects.get(id=slug)
                if project.author.username == logged_in_user.username:
                    project.delete()
                    return JsonResponse({'message': f'Project deleted successfully with id {slug}'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return JsonResponse({'message': 'You are not authorized to delete this project'}, status=status.HTTP_401_UNAUTHORIZED)
            except Projects.DoesNotExist:
                return JsonResponse({'message': f'Project not found with the id {slug}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'Please provide the project id'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listProjectOfUser(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
            if user is None:
                return JsonResponse({'message': f'User not found with the username {username}'}, status=status.HTTP_404_NOT_FOUND)
            
            projects = Projects.objects.filter(author=user.username)
            serializer = ProjectSerializer(projects, many=True)
            return JsonResponse({
                "data": serializer.data,
                "message": f'Projects found successfully for the user {username}',
                'server': 'db'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse({'message': f'User not found with the username {username}'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'Please provide the username'}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def likeproject(request, slug=None):
    print("someone wants to like a project")
    if slug:
        try:
            token_type, token = request.headers['Authorization'].split(' ')
            logged_in_user = get_current_user(token)
            project = Projects.objects.get(slug=slug)
            # check if the user has already liked the project or not
            if logged_in_user.username in project.upvotes.all().values_list('username', flat=True):
                print("user has already liked this project")
                project.upvotes.remove(logged_in_user.username)
                logged_in_user.karma -= 15
                project.save()
                logged_in_user.save()
                return JsonResponse({
                    'message': 'Unliked the project 😭',
                    "action": "unliked",
                    "status": "success",
                    "likecount": project.upvotes.count(),
                    "description": "ooh! you don't like this project anymore 🥲"
                }, status=status.HTTP_200_OK)
            else:
                print("user has not liked this project")
                project.upvotes.add(logged_in_user.username)
                project.save()
                logged_in_user.karma += 15
                logged_in_user.save()
                
                return JsonResponse({
                    'message': 'You have liked this project 😇',
                    "action": "liked",
                    "status": "success",
                    "likecount": project.upvotes.count(),
                    "description": "Go to your profile to see your liked projects 👀"
                }, status=status.HTTP_200_OK)
        except Projects.DoesNotExist:
            return JsonResponse({'message': f'Project not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'Please provide the project slug'}, status=status.HTTP_400_BAD_REQUEST)


# make similar for bookmarks
@api_view(['GET'])
def bookmarkproject(request, slug=None):
    if slug:
        try:
            token_type, token = request.headers['Authorization'].split(' ')
            logged_in_user = get_current_user(token)
            project = Projects.objects.get(slug=slug)

            if logged_in_user.username in project.bookmarks.all().values_list('username', flat=True):
                project.bookmarks.remove(logged_in_user.username)
                project.save()
                return JsonResponse({
                    'message': 'Removed from bookmarks 👋',
                    "action": "unbookmarked",
                    "status": "success",
                    "bookmarkcount": project.bookmarks.count(),
                    "description": "ooh! you don't have this project bookmarked anymore 🥲"
                }, status=status.HTTP_200_OK)
            else:
                project.bookmarks.add(logged_in_user.username)
                project.save()
                return JsonResponse({
                    'message': 'Added to bookmarks 🎉',
                    "action": "bookmarked",
                    "status": "success",
                    "bookmarkcount": project.bookmarks.count(),
                    "description": "Go to your profile to see your bookmarked projects 👀"
                }, status=status.HTTP_200_OK)
        except Projects.DoesNotExist:
            return JsonResponse({'message': f'Project not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'Please provide the project slug'}, status=status.HTTP_400_BAD_REQUEST)


# make similar for views
@api_view(['GET'])
def viewproject(request, slug=None):
    if slug:
        try:
            token_type, token = request.headers['Authorization'].split(' ')
            logged_in_user = get_current_user(token)
            project = Projects.objects.get(slug=slug)

            if logged_in_user.username in project.views.all().values_list('username', flat=True):
                return JsonResponse({
                    'message': 'You have already viewed this project 😇',
                    "action": "viewed",
                    "status": "success",
                    "likecount": project.views.count(),
                    "description": "Go to your profile to see your viewed projects 👀"
                }, status=status.HTTP_200_OK)
            else:
                project.bookmarks.add(logged_in_user.username)
                project.save()
                return JsonResponse({
                    'message': 'Viewed this project 🎉',
                    "action": "viewed",
                    "status": "success",
                    "likecount": project.views.count(),
                    "description": "Go to your profile to see your viewed projects 👀"
                }, status=status.HTTP_200_OK)
        except Projects.DoesNotExist:
            return JsonResponse({'message': f'Project not found with the slug {slug}'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'Please provide the project slug'}, status=status.HTTP_400_BAD_REQUEST)


