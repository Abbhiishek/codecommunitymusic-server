
from django.urls import path, include
from .views import *
from app.Views.LoginSignupView import *
from app.Views.UserView import *
from app.Views.ProjectView import *
from app.Views.ForumView import *
from app.Views.LeaderboardView import *
from app.Views.TodoView import *
from app.Views.BlogView import *
from app.Views.ChatView import *
urlpatterns = [
    path('routes', getallavailableroutes, name='Get all available routes'),
    path('randomprogrammingquote', getrandomprogrammingquote, name='Get random programming quote'),
    
    ## users urls
    path('getalluserusername' ,  getalluserusername , name='Get all user username'),
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

    path('projects/<str:slug>', project, name='projects - GET, POST, PUT, DELETE'),
    path('like/project/<str:slug>', likeproject, name='Like project'),
    path('bookmark/project/<str:slug>', bookmarkproject, name='Bookmark project'),
    path('list/projects', allprojects, name='all projects - without auth'),
    path('list/<str:username>/projects', listProjectOfUser, name='List projects of user with username'),

    # forum urls
    path('forums', fetch_all_forums, name='discussions - GET'),
    path('forums/<str:slug>', fetch_forum, name='discussions - GET,'),
    path('create/forums', create_forum, name='discussions -  POST'),
    path('update/forums/<str:slug>', update_forum, name='discussions -  PUT'),
    path('delete/forums/<str:slug>', delete_forum, name='discussions -  DELETE'),
    path('list/<str:username>/forums', listForumOfUser, name='discussions -  like'),
    path('list/forums', fetch_all_forums, name='discussions -  like'),


    ## chats urls
    path('create/forums/<str:slug>/chat', postanswerforforum, name='chats - Post'),
    path('delete/forums/<str:slug>/chat/<str:id>', deleteanswerforforum, name='chats -  Delete'),

    # todos urls
    path('user/<str:username>/todos', gettodo, name='todos - GET , post'),
    path('user/<str:username>/todos/<str:todo_id>', deletetodo, name='todos - delete'),
    path('user/<str:username>/todos/<str:todo_id>/update', updatetodo, name='todos - update'),

    #  blogs urls
    path('blogs/<str:slug>', get_blog, name='blogs - GET'),
    path('create/blogs', create_blog, name='blogs - Post'),
    path('update/blogs/<str:slug>', update_blog, name='blogs -  PUT'),
    path('delete/blogs/<str:slug>', delete_blog, name='blogs -  DELETE'),
    path('list/<str:username>/blogs', listBlogOfUser, name='blogs -  like'),

    ## leaderboard urls
    path('leaderboard', leaderboard, name='leaderboard - GET'),
]
