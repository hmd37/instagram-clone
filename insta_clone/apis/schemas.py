from drf_spectacular.utils import (
    extend_schema_view, extend_schema,
)

from posts.serializers import PostSerializer

from users.serializers import UserRegisterSerializer


user_register_schema = extend_schema_view(
    post=extend_schema(
        request=UserRegisterSerializer,
        responses={201: {"message": "User registered successfully"}},
        description="Register a new user",
        tags=["Register"]
    )
)


post_list_create_schema = extend_schema_view(
    get=extend_schema(
        summary="List and create posts",
        description="GET: Retrieves posts from users that the current user follows, ordered by creation date.\n"
                   "POST: Creates a new post for the current authenticated user.",
        responses={
            200: PostSerializer(many=True),
            201: PostSerializer,
        },
        tags=["Posts"]
    ),
    post=extend_schema(
        summary="Create a new post",
        description="Creates a new post associated with the current authenticated user.",
        request=PostSerializer,
        responses={201: PostSerializer},
        tags=["Posts"]
    )
)
