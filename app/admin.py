from django.contrib import admin



from .Models.models import *


# admin.site.register(User)
# admin.site.register(Discussions)
# admin.site.register(Projects)
# admin.site.register(Comments)


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')


@admin.register(Forum)
class DiscussionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author')


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



