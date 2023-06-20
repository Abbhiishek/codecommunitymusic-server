
from django.urls import path, include
from .views import *
from app.Views.LoginSignupView import *
from app.Views.UserView import *
from app.Views.ProjectView import *
from app.Views.ForumView import *
from app.Views.LeaderboardView import *
from app.Views.ChatView import *


urlpatterns = [
    path('routes', getallavailableroutes, name='Get all available routes'),
    
    ## users urls
    path('users/<str:username>', users, name='Get all users'),
    path('users', users, name='Get all users'),
    path('getuser', getuser, name='Get user by session_token'),
    path('generateotp/<str:username>', generateotp, name='Generate OTP'),
    path('verifyaccount/<str:username>', verifyaccount, name='Verify account'),
    path('updateuser', updateuser, name='Update user'),
    path('user/changepassword/<str:email>', updatepassword, name='Change password'),
    path('user/forgetpassword/<str:email>', forgetpassword, name='Forget password'),
    path('followuser/<str:username>', followuser, name='Follow user'),



    # signup
    path('register', createuser, name='Create user'),


    # login
    path('login', login, name='Login user'),
    path('directlogin', directLogin, name='Login user with just email'),

    # projects urls
    path('projects', project, name='projects - GET, POST, PUT, DELETE'),
    path('getallprojects', allprojects, name='all projects - without auth'),
    path('projects/<str:slug>', project,
         name='projects - GET, POST, PUT, DELETE'),
    path('like/project/<str:slug>', likeproject, name='Like project'),
    path('bookmark/project/<str:slug>', bookmarkproject, name='Bookmark project'),

    path('user/<str:username>/projects', listProjectOfUser, name='List projects of user with username'),




     ## forum urls
     path('forums', forum, name='discussions - GET, POST, PUT, DELETE'),
     path('forums/<str:slug>', forum,
         name='discussions - GET, POST, PUT, DELETE'),

     ## chat urls
     path('forum/<str:forum_slug>/chat', chat, name='chat - GET , post'),


     ## leaderboard urls
     path('leaderboard', leaderboard, name='leaderboard - GET'),
]
