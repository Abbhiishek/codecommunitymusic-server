
# craete a new file called oauth2.py
# this file will contain the logic for the OAuth2 server
# like hasghing the password, generating the access token, etc.

# import the required libraries and modules the project is in django rest framework
# so we will import the rest_framework library


import datetime
import jwt
from app.Models.Users import User
from core import settings
from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


def generateJWTToken(email, username):
    # this function will generate the access token
    # we will use the jwt library to generate the token
    # we will pass the username and password to this function
    # and it will return the access token
    # we will use the SECRET_KEY from the settings.py file
    # to generate the token
    # we will use the HS256 algorithm to generate the token
    # we will use the datetime library to generate the expiry time
    # for the token

    expiry_time = datetime.datetime.now() + datetime.timedelta(days=30)
    token = jwt.encode({'username': username, 'email': email, 'exp': expiry_time},
                       settings.SECRET_KEY, algorithm='HS256')
    return token


def verifyJWTToken(token):
    """
    This function will verify the token
    :param token:
    :return: decoded_token
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def refreshJWTToken(token):
    """
    This function will refresh the token
    :param token:
    :return: token(NEW REFRESHED TOKEN)
    """

    decoded_token = jwt.decode(
        token, settings.SECRET_KEY, algorithms=['HS256'])
    decoded_token['exp'] = datetime.datetime.utcnow() + \
        datetime.timedelta(days=30)
    token = jwt.encode(decoded_token, settings.SECRET_KEY, algorithm='HS256')
    return token


def get_current_user(token):
    """
    This function will return the current user from the token passed
    """
    # this function will return the current user from the token passed
    # we will use the verifyJWTToken function to verify the token and get the username
    # we will use the User model to get the user from the username
    # we will return the user object
    # if the token is invalid or expired, we will return a 401 status cdde

    decoded_token = verifyJWTToken(token)
    email = decoded_token.get('email')
    user = User.objects.get(email=email)
    return user


class JWTAuthenticationMiddleware:
    """
    This middleware will check for the token in the request header
    and will verify the token
    """

    EXCLUDED_PATHS = [
        '/login',
        '/register',
        '/admin',
        '/routes',
        '/directlogin',
        '/getallprojects',
        '/getalluserusername',
        '/user/forgetpassword',
        '/user/changepassword',
        '/static/admin',
        # Add other paths that don't require JWT token verification
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def is_excluded_path(self, request):
        for path in self.EXCLUDED_PATHS:
            if request.path.startswith(path):
                return True
        return False

    def __call__(self, request):
        if self.is_excluded_path(request):
            return self.get_response(request)

        authorization_header = request.headers.get('AUTHORIZATION')
        if authorization_header:
            token_type, token = authorization_header.split(' ')
            print("-----------------")
            print(token_type, token)
            if token_type.lower() == 'bearer':
                try:
                    payload = verifyJWTToken(token)
                    if payload == None:
                        return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
                    print("payload after encrypting : ", payload)
                    loggedinuser = get_current_user(token)
                    print("Request made by : ", loggedinuser.username)
                    currentuser = User.objects.get(
                        username=loggedinuser.username)
                    print("Current user : ", currentuser.username)
                    if not currentuser:
                        return JsonResponse({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
                    return self.get_response(request)
                except:
                    return JsonResponse({'message': 'Invalid Request, No auth token passed'}, status=status.HTTP_401_UNAUTHORIZED)
        return JsonResponse({'message': 'Invalid Request, Bearer token not found or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
