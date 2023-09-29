import random
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from app.libs.oauth2 import get_current_user
from app.Serializers.UserSerializer import UserSerializer , AllUserSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from app.Models.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from core.settings import EMAIL_HOST_USER
from datetime import datetime

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['GET'])
def users(request, username=None):
    # username = request.query_params.get('username')
    starttime = datetime.now()
    if request.method == 'GET':
        if username:
            try:
                cached_user = cache.get(username)
                if cached_user is None:
                    user = User.objects.get(username=username)
                    serializer = UserSerializer(user)
                    cache.set(username, serializer.data, timeout=0)
                    endtime = datetime.now()
                    return JsonResponse({
                        "data": serializer.data,
                        "message": f'User found successfully with username {username}',
                        "time_taken": str(endtime - starttime),
                        "server": "db"
                    }, status=status.HTTP_200_OK)
                else:
                    endtime = datetime.now()
                    return JsonResponse({
                        "data": cached_user,
                        "message": f'User found successfully with username {username}',
                        "time_taken": str(endtime - starttime),
                        "server": "cache server v2"
                    }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the username {username}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cached_users = cache.get('allusers')
            if cached_users is None:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                cache.set('allusers', serializer.data, timeout=65)
                endtime = datetime.now()
                return JsonResponse({
                    "data": serializer.data,
                    "message": "success",
                    "time_taken": str(endtime - starttime),
                    "server": "db"
                }, status=status.HTTP_200_OK)
            else:
                endtime = datetime.now()
                return JsonResponse({
                    "data": cached_users,
                    "message": "success",
                    "time_taken": str(endtime - starttime),
                    "server": "cache server v2"
                }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getuser(request):

    session_token = request.headers.get('Authorization').split(' ')[1]
    if session_token:
        user = cache.get(session_token)
        if user is None:
            current_user = get_current_user(session_token)
            serializer = UserSerializer(current_user)
            if current_user:
                cache.set(session_token, serializer.data, timeout=0)
                return JsonResponse({'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'data': user}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateuser(request):
    session_token = request.headers.get('Authorization').split(' ')[1]
    if session_token:
        current_user = get_current_user(session_token)
        if current_user:
            serializer = UserSerializer(instance=current_user, data=request.data , partial=True)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Invalid request serialiser failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'Invalid request oops no seesion token'}, status=status.HTTP_400_BAD_REQUEST)

## todo 1:  verify account with a otp as post body and compare with the otp in user model
@api_view(['POST'])
def verifyaccount(request , username=None):
    if request.method == 'POST':
        token = request.headers.get('Authorization').split(' ')[1]
        if token:
            ## check if ther person requesting has the same usernmae as the one he is trying to verify
            current_user = get_current_user(token)
            if current_user.username != username:
                return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        ## check if ther person is already verified
        user = User.objects.get(username=username)
        if user.is_verified:
            return JsonResponse({
                'message': 'Account already verified ✅',
                'description': 'You are already a verified user 🥳',
                'status': 'success'
            }, status=status.HTTP_200_OK)
        
        if username:
            try:
                user = User.objects.get(username=username)
                otp = request.data.get('otp')
                if user.is_verified:
                    return JsonResponse({
                            'message': 'Account already verified ✅',
                            'description': 'You are already a verified user 🥳',
                            'status': 'success'
                        }, status=status.HTTP_200_OK)
                if str(user.temp_otp) == otp:
                    user.is_verified = True
                    user.temp_otp = None
                    user.save()
                    return JsonResponse({
                        'message': 'Account verified successfully ✅',
                        'description': 'You are now a verified user 🥳',
                        'status': 'success'
                    }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the username {username}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


## Todo 1 :  generate otp and save that to user model and send a email to user's email address

@api_view(['GET'])
def generateotp(request , username=None):

    if request.method == 'GET':
        token = request.headers.get('Authorization').split(' ')[1]
        if token:
            ## check if ther person requesting has the same usernmae as the one he is trying to verify
            current_user = get_current_user(token)
            if current_user.username != username:
                return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        ## check if ther person is already verified
        user = User.objects.get(username=username)
        if user.is_verified:
            return JsonResponse({
                'message': 'Account already verified ✅',
                'description': 'You are already a verified user 🥳',
                'status': 'success'
            }, status=status.HTTP_200_OK)
        if username:
            try:
                user = User.objects.get(username=username)
                if user.is_verified:
                    return JsonResponse({
                            'message': 'Account already verified ✅',
                            'description': 'You are already a verified user 🥳',
                            'status': 'success'
                        }, status=status.HTTP_200_OK)
                otp = random.randint(100000, 999999)
                user.temp_otp = otp
                
                user.save()
                send_mail(
                subject=f'Verify your account {user.username}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
                message='Verify your account',
                html_message=f'''
                <h1>Verify your account</h1>
                <p>Hi {user.username},</p>
                <p>Thanks for signing up for CodeCommunity Music! We're excited to have you as an early user.</p>
                <p>Use the following OTP to verify your account</p>
                <h2>{user.temp_otp}</h2>
                <p>Thanks,</p>
                <p>The CodeCommunity Music Team</p>
                ''')
                return JsonResponse({
                    'message': 'OTP generated successfully ✅',
                    'description': 'OTP generated successfully and sent to your email address 🥳',
                    'status': 'success'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the username {username}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'no username is passed :('}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'only post is allowed'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET' , 'POST'])
def forgetpassword(request, email=None):
    if request.method == 'GET':
        if email:
            try:
                user = User.objects.get(email=email)
                otp = random.randint(100000, 999999)
                user.reset_password_token = str(otp)
                user.save()
                send_mail(
                subject=f'Verify your account {user.username}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
                message='Reset your password',
                html_message=f'''
                <h1>
                    Reset your password
                </h1>
                <p>Hi {user.username},</p>
                <p>
                    We have received a request to reset your password. If you did not make this request, simply ignore this email. Otherwise, please use the following OTP to reset your password.
                </p>
                <h2>{user.reset_password_token}</h2>
                <p>Use the following OTP to reset your password</p>
                <h2>
                The OTP will expire in 15 minutes
                </h2>
                <p>Thanks,</p>
                <p>The CodeCommunity Music Team</p>
                ''')
                return JsonResponse({
                    'message': 'OTP generated successfully ✅',
                    'description': 'OTP generated successfully and sent to your email address 🥳',
                    'status': 'success'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the email {email}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'no username is passed :('}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        if email:
            try:
                user = User.objects.get(email=email)
                otp = request.data.get('otp')
                if otp:
                    if user.reset_password_token == otp:
                            return JsonResponse({
                                'message': 'OTP verified successfully ✅',
                                'description': 'OTP verified successfully 🥳',
                                'status': 'success',
                                "success": True
                            }, status=status.HTTP_200_OK)
                    else:
                        return JsonResponse({
                            'message': 'OTP is incorrect ❌',
                            'description': 'OTP is incorrect 🥺',
                            'status': 'failed'
                        }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return JsonResponse({
                        'message': 'OTP is not passed ❌',
                        'description': 'OTP is not passed 🥺',
                        'status': 'failed'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the email {email}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'no username is passed :('}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updatepassword(request , email=None):
    if request.method == 'PUT':
        if email:
            try:
                user = User.objects.get(email=email)
                password = request.data.get('password')
                if password:
                    hashed_password = make_password(password)
                    user.password = hashed_password
                    user.save()
                    send_mail(
                    subject=f'Password updated {user.username}',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                    message='Password updated',
                    html_message=f'''
                    <h1>
                        Password updated
                    </h1>
                    <p>Hi {user.username},</p>
                    <p>
                        Your password has been updated successfully.
                    </p>
                    <p>Thanks,</p>
                    <p>The CodeCommunity Music Team</p>
                    ''')
                    return JsonResponse({
                        'message': 'Password updated successfully ✅',
                        'description': 'Password updated successfully 🥳',
                        'status': 'success'
                    }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({
                        'message': 'Password is not passed ❌',
                        'description': 'Password is not passed 🥺',
                        'status': 'failed'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the email {email}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'no email is passed :('}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'only put is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def followuser(request , username=None):
    if request.method == 'GET':
        if username:
            try:
                token = request.headers.get('Authorization').split(' ')[1]
                current_user = get_current_user(token)
                user = User.objects.get(username=username)
                if current_user.username == user.username:
                    return JsonResponse({
                        'message': 'You can not follow yourself ❌',
                        'description': 'You can not follow yourself 👀',
                        'status': 'failed'
                    }, status=status.HTTP_400_BAD_REQUEST)
                if user:
                    if current_user.following.filter(username=user.username).exists():
                        current_user.following.remove(user)
                        user.followers.remove(current_user)
                        user.save() 
                        current_user.save()
                        return JsonResponse({
                            'message': 'User unfollowed successfully ✅',
                            'description': 'User unfollowed successfully ',
                            'status': 'success',
                            'action': 'unfollowed'
                        }, status=status.HTTP_200_OK)
                    else:
                        current_user.following.add(user)
                        user.followers.add(current_user)
                        user.save()
                        current_user.save()
                        return JsonResponse({
                            'message': 'User followed successfully ✅',
                            'description': 'User followed successfully 🥳',
                            'status': 'success',
                            'action': 'followed'
                        }, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({
                        'message': 'User not found ❌',
                        'description': 'User not found 🥺',
                        'status': 'failed'
                    }, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return JsonResponse({'message': f'User not found with the username {username}'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'no username is passed :('}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': 'only get is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    




@api_view(['GET'])
def getalluserusername(request):
    if request.method == 'GET':
        try:
            users = User.objects.all()
            serializer = AllUserSerializer(users, many=True)
            return JsonResponse({'users': serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse({'message': 'No users found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return JsonResponse({'message': 'only get is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)