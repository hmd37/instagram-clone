from django.urls import reverse

from drf_spectacular.utils import extend_schema_field

from rest_framework import serializers

from .models import Post, Comment

MB = 1024 * 1024


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') 

    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'post', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username') 
    likes_count = serializers.IntegerField(read_only=True)  
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['url', 'id', 'user', 'image', 'caption', 
                  'likes_count', 'comments_count']
    
    @extend_schema_field(serializers.CharField())
    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('post-detail', kwargs={'post_id': obj.id})
        )
    
    def validate_image(self, value):
        if value.size > 2 * MB: 
            raise serializers.ValidationError("Image file size must be less than 2MB.")
        if not value.name.lower().endswith(('jpg', 'png')):
            raise serializers.ValidationError("Only JPG and PNG formats are allowed.")
        return value
    

class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True) 

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 
                  'created_at', 'likes_count', 'comments_count', 'comments']
