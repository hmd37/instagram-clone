from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post, Like, Comment

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        """Set up test users and posts."""
        self.user = User.objects.create_user(
            username="testuser", email="user1@example.com", password="password123"
        )
        self.post = Post.objects.create(user=self.user, caption="This is a test post.")

    def test_create_post(self):
        """Ensure a post can be created successfully."""
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.caption, "This is a test post.")
        self.assertFalse(bool(self.post.image))  

    def test_post_deletion_cascades(self):
        """Ensure deleting a user also deletes their posts."""
        self.user.delete()
        self.assertEqual(Post.objects.count(), 0)


class LikeModelTest(TestCase):
    def setUp(self):
        """Set up users and a post for testing likes."""
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password123"
        )
        self.post = Post.objects.create(user=self.user1, caption="Post to be liked.")

    def test_create_like(self):
        """Ensure a like can be created successfully."""
        like = Like.objects.create(user=self.user2, post=self.post)
        self.assertEqual(like.user, self.user2)
        self.assertEqual(like.post, self.post)

    def test_prevent_duplicate_likes(self):
        """Ensure a user cannot like the same post twice."""
        Like.objects.create(user=self.user2, post=self.post)
        with self.assertRaises(Exception):  
            Like.objects.create(user=self.user2, post=self.post)

    def test_like_deletion_cascades(self):
        """Ensure deleting a post removes associated likes."""
        Like.objects.create(user=self.user2, post=self.post)
        self.post.delete()
        self.assertEqual(Like.objects.count(), 0)


class CommentModelTest(TestCase):
    def setUp(self):
        """Set up users and posts for testing comments."""
        self.user = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.post = Post.objects.create(user=self.user, caption="A post with comments.")
        self.comment = Comment.objects.create(user=self.user, post=self.post, text="Nice post!")

    def test_create_comment(self):
        """Ensure a comment can be created successfully."""
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.text, "Nice post!")

    def test_comment_deletion_cascades(self):
        """Ensure deleting a post also deletes associated comments."""
        self.post.delete()
        self.assertEqual(Comment.objects.count(), 0)

