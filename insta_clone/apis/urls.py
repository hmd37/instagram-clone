from django.urls import path

from .views import (
    UserListAPIView, UserDetailAPIView,
    FollowToggleView, PostListCreateAPIView,
    PostDetailAPIView, LikeToggleView,
    CommentListCreateAPIView,
)


urlpatterns = [
    path(
        "users/", 
        UserListAPIView.as_view(), 
        name='users'
    ),
    path(
        "users/<str:username>/", 
        UserDetailAPIView.as_view(), 
        name='user-detail'
    ),
    path(
        "users/<str:username>/follow/", 
        FollowToggleView.as_view(), 
        name='follow'
    ),
    path(
        "posts/",
        PostListCreateAPIView.as_view(),
        name='posts'
    ),
    path(
        "posts/<int:post_id>/",
        PostDetailAPIView.as_view(),
        name='post-detail'
    ),
    path(
        "posts/<int:post_id>/like/",
        LikeToggleView.as_view(),
        name='like'
    ),
    path(
        "posts/<int:post_id>/comments/",
        CommentListCreateAPIView.as_view(),
        name='comments'
    )
]
