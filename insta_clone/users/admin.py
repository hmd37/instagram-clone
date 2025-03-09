from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'followers_count', 'following_count', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ('followers_count', 'following_count')

    fieldsets = (
        ('Basic Info', {'fields': ('username', 'email', 'password', 'profile_picture', 'bio')}),
        ('Followers', {'fields': ('followers_count', 'following_count')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    def followers_count(self, obj):
        return obj.followers.count()
    followers_count.short_description = "Followers"

    def following_count(self, obj):
        return obj.following.count()
    following_count.short_description = "Following"

admin.site.register(User, CustomUserAdmin)
