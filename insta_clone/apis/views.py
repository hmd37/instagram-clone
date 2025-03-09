from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer

from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, CommentSerializer


#Users
class UserRegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, 
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response({"message": "User deleted successfully"}, 
                        status=status.HTTP_204_NO_CONTENT)


class FollowToggleView(APIView):

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
class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Post.objects.none() 

        followed_users = user.following.all()  
        return Post.objects.filter(user__in=followed_users).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(APIView):

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if request.user != post.user:
            return Response({"error": "You can only delete your own posts"}, 
                            status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": "Post deleted successfully"}, 
                        status=status.HTTP_204_NO_CONTENT)
    

class LikeToggleView(APIView):

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
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)  
        serializer.save(user=self.request.user, post=post)

    