from django.contrib import admin



from .Models.models import *


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')


@admin.register(Forum)
class DiscussionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'author')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')
    


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_verified', 'created_at', 'updated_at')
    list_filter = ('username', 'email', 'first_name', 'last_name',
                   'is_active', 'is_verified', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'first_name', 'last_name',
                     'is_active', 'is_verified', 'created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'updated_at')



@admin.register(LearningPath)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')



@admin.register(SubCourse)
class SubCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')