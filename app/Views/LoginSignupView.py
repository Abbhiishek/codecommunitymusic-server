from datetime import datetime
from django.db.models import Q
from app.libs.oauth2 import generateJWTToken
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from app.serializers import UserSerializer
from app.Models.models import User
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER


# local

@api_view(['POST'])
def createuser(request):
    """
    Create a new user.
    """
    if request.method == 'POST':
        password = request.data['password']
        hashed_password = make_password(password)
        request.data['password'] = hashed_password
        request.data['karma'] = 50
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            session_token = generateJWTToken(
                username=serializer.data.get("username"), email=serializer.data.get("email"))
            send_mail(
                subject=f'Welcome {serializer.data.get("username")} to CodeCommunityMusic',
                from_email=EMAIL_HOST_USER,
                recipient_list=[serializer.data.get("email")],
                fail_silently=False,
                message='Welcome to CodeCommunityMusic. We are glad to have you here.',
                html_message=f'''
                <h4>Hi {serializer.data.get("username")}</h4>
                <p>We're so excited to have you join our community of developers who are passionate about coding and helping others.</p>
                <p>Here are a few things you can do to get started:</p>
                <ul>
                    <li>Explore our forums and chat rooms to connect with other developers and learn from each other.</li>
                    <li>Browse our library of coding resources, including tutorials, articles, and code samples.</li>
                    <li>Verify your account to gain access to our full range of features.</li>
                </ul>
                <p>Please click on the following link to verify your account:</p>
                <a href='https://codecommunitymusic.vercel.app/verify'>Verify Account</a>
                <p>We're always looking for new ways to help our members, so please don't hesitate to reach out if you have any questions or suggestions.</p>
                <p>Thanks for joining CodeCommunity Music!</p>
                <br>
                <p>Sincerely,</p>
                <p>The CodeCommunity Music Team</p>
                '''
            )
            return JsonResponse({
                'message': f'''User created successfully with {serializer.data.get("username")}''',
                'data': serializer.data,
                "status": "success",
                "session_token": session_token
            }, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'Invalid request Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        start_time = datetime.now()
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(
            Q(username=username) or Q(email=username)).first()
        if user:
            serializer = UserSerializer(user)
            user.karma += 10
            user.save()
            print( "karmn updated to " , user.karma)
            if check_password(password, user.password):
                session_token = generateJWTToken(
                    username=username, email=user.email)
                end_time = datetime.now()
                return JsonResponse({
                    "message": "User logged in successfully",
                    "status": "success",
                    "time_taken": end_time - start_time,
                    "data": serializer.data,
                    "session_token": session_token
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Wrong password! Try Again'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'User not found with the Credintials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'Invalid request Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def directLogin(request):
    if request.method == 'POST':
        start_time = datetime.now()
        email = request.data['email']
        user = User.objects.filter(Q(email=email)).first()
        if user:
            serializer = UserSerializer(user)
            session_token = generateJWTToken(
                username=user.username, email=user.email)
            end_time = datetime.now()
            return JsonResponse({
                "message": "User logged in successfully",
                "status": "success",
                "time_taken": end_time - start_time,
                "data": serializer.data,
                "session_token": session_token
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'User not found with the Credintials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'Invalid request Method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
