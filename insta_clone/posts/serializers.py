from rest_framework import serializers

from .models import Post, Comment
from django.urls import reverse

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') 

    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'post', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username') 
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['url', 'id', 'user', 'image', 'caption', 
                  'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('post-detail', kwargs={'post_id': obj.id}))
    

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True) 

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 
                  'created_at', 'likes_count', 'comments_count', 'comments']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()
