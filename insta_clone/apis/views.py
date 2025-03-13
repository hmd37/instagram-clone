from django.db.models import Count
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.permissions import IsProfileOwnerOrAdmin, IsPostOwnerOrAdmin
from apis.schemas import user_register_schema, post_list_create_schema

from users.models import User
from users.serializers import (
    UserSerializer, UserDetailSerializer,
    UserRegisterSerializer,
)

from posts.models import Post, Like, Comment
from posts.serializers import (
    PostSerializer, PostDetailSerializer,
    CommentSerializer, 
)


#Users
@user_register_schema
class UserRegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_serializer(self, *args, **kwargs):
        return UserRegisterSerializer(*args, **kwargs)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username',]

    queryset = User.objects.annotate(
        followers_count=Count('followers', distinct=True),
        following_count=Count('following', distinct=True)
    ).order_by('-date_joined')
    serializer_class = UserSerializer


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrAdmin]

    def get_serializer(self, *args, **kwargs):
        return UserDetailSerializer(*args, **kwargs)
    
    def get(self, request, username):
        user = get_object_or_404(
            User.objects.annotate(
                followers_count=Count('followers', distinct=True),
                following_count=Count('following', distinct=True)
            ),
            username=username
        )
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserDetailSerializer(user, data=request.data, partial=True)

        self.check_object_permissions(request, user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)

        self.check_object_permissions(request, user)
        
        user.delete()
        return Response({"message": "User deleted successfully"}, 
                        status=status.HTTP_204_NO_CONTENT)


class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(exclude=True)
    def post(self, request, username):
        """Toggle follow/unfollow action."""
        target_user = get_object_or_404(User, username=username)

        if request.user == target_user:
            return Response({"error": "You cannot follow yourself"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        if request.user in target_user.followers.all():
            target_user.followers.remove(request.user)
            message = "Unfollowed successfully"
        else:
            target_user.followers.add(request.user)
            message = "Followed successfully"

        return Response({
                "message": message, 
                "is_following": request.user in target_user.followers.all()
            }, 
             status=status.HTTP_200_OK
            )


#Posts
@post_list_create_schema
class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Post.objects.none()

        followed_users = user.following.all()

        return (
            Post.objects.filter(user__in=followed_users)
            .annotate(
                likes_count=Count('likes', distinct=True),
                comments_count=Count('comments', distinct=True)
            )
            .select_related('user') 
            .order_by('-created_at')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsPostOwnerOrAdmin]
    serializer_class = PostDetailSerializer

    def get(self, request, post_id):
        post = get_object_or_404(
        Post.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )
        .select_related('user') 
        .prefetch_related('comments__user') 
        , id=post_id
        )

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        self.check_object_permissions(request, post) 

        post.delete()
        return Response({"message": "Post deleted successfully"}, 
                        status=status.HTTP_204_NO_CONTENT)
    

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(exclude=True)
    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()
            return Response({"message": "Unliked post"}, 
                            status=status.HTTP_200_OK)

        return Response({"message": "Liked post"}, 
                        status=status.HTTP_201_CREATED)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)  
        serializer.save(user=self.request.user, post=post)
