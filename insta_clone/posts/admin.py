from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'caption', 'created_at',)
    list_filter = ('created_at', 'user')
    search_fields = ('caption', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    inlines = [] 


class CommentInline(admin.TabularInline):  
    model = Comment
    extra = 1  
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text', 'created_at')
    list_filter = ('created_at', 'user', 'post')
    search_fields = ('text', 'user__username', 'post__caption')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


PostAdmin.inlines.append(CommentInline)
