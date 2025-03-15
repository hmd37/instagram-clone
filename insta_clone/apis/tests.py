from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, Like

User = get_user_model()


class UserRegisterAPITestCase(APITestCase):

    def setUp(self):
        """Set up a test user for authentication."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.register_url = reverse("register")  
        self.user_list_url = reverse("users")  

    def test_register_user_success(self):
        """Test user registration with valid data."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_register_user_fail(self):
        """Test user registration failure due to missing data."""
        data = {
            "username": "incompleteuser"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data) 


class UserListAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1', email='user1@gmail.com')
        self.user2 = User.objects.create_user(username='user2', password='password2', email='user2@gmail.com')
        self.user3 = User.objects.create_user(username='user3', password='password3', email='user3@gmail.com')
        self.auth_user = User.objects.create_user(username='auth_user', password='auth_password', email='auth@gmail.com')

        self.user1.followers.add(self.user2)
        self.user1.followers.add(self.user3)

        self.user_list_url = reverse('users')  

    def test_permission_required(self):
        """Test that the view requires authentication (IsAuthenticated)."""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_list_authenticated(self):
        """Test that authenticated users can retrieve the user list."""
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_filter(self):
        """Test that searching for users by username works."""
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(self.user_list_url + '?search=user1')
        
        self.assertTrue('results' in response.data)
        self.assertIsInstance(response.data['results'], list)
        
        self.assertEqual(len(response.data['results']), 1) 
        self.assertEqual(response.data['results'][0]['username'], 'user1')
    
    def test_search_no_results(self):
        """Test that searching for a non-existent username returns an empty list."""
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(self.user_list_url + '?search=nonexistentuser')
        
        self.assertTrue('results' in response.data)
        self.assertIsInstance(response.data['results'], list)
        
        self.assertEqual(len(response.data['results']), 0)


class UserDetailAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1', email='user1@gmail.com')
        self.user2 = User.objects.create_user(username='user2', password='password2', email='user2@gmail.com')
        self.admin = User.objects.create_user(username='admin', password='adminpassword', email='admin@example.com', is_staff=True)

        self.user_detail_url = reverse('user-detail', kwargs={'username': 'user1'})

    def test_permission_required(self):
        """Test that the view requires authentication (IsAuthenticated)."""
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_authenticated(self):
        """Test that an authenticated user can retrieve their own user details."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('user-detail', kwargs={'username': 'user1'}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')

    def test_put_user_detail_authenticated_owner(self):
        """Test that an authenticated user can update their own user details."""
        self.client.force_authenticate(user=self.user1)
        updated_data = {'bio': 'Updated bio'}
        response = self.client.put(reverse('user-detail', kwargs={'username': 'user1'}), updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')

    def test_put_user_detail_authenticated_non_owner(self):
        """Test that a user cannot update another user's details."""
        self.client.force_authenticate(user=self.user1)
        updated_data = {'bio': 'Updated bio'}
        response = self.client.put(reverse('user-detail', kwargs={'username': 'user2'}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_user_detail_authenticated_admin(self):
        """Test that an admin can update another user's details."""
        self.client.force_authenticate(user=self.admin)
        updated_data = {'bio': 'Updated bio by admin'}
        response = self.client.put(reverse('user-detail', kwargs={'username': 'user2'}), updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio by admin')

    def test_delete_user_detail_authenticated_owner(self):
        """Test that an authenticated user can delete their own user account."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('user-detail', kwargs={'username': 'user1'}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_detail_authenticated_admin(self):
        """Test that an admin can delete any user's account."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse('user-detail', kwargs={'username': 'user2'}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_user_detail_authenticated_non_owner(self):
        """Test that a user cannot delete another user's account."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('user-detail', kwargs={'username': 'user2'}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_detail_non_existent_user(self):
        """Test that a request for a non-existent user returns a 404 error."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('user-detail', kwargs={'username': 'nonexistentuser'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FollowToggleViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        self.url = reverse('follow', kwargs={'username': self.user2.username})

    def test_follow(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user2.followers.filter(id=self.user1.id).exists())

    def test_unfollow(self):
        self.user2.followers.add(self.user1)
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user2.followers.filter(id=self.user1.id).exists())

    def test_follow_self(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('follow', kwargs={'username': self.user1.username})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_without_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostListCreateAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        self.user1.following.add(self.user2)
        self.post1 = Post.objects.create(user=self.user1, image='image1.jpg', caption='caption1')
        self.post2 = Post.objects.create(user=self.user2, image='image2.jpg', caption='caption2')
        self.url = reverse('posts')

    def test_get_posts(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  

    def test_get_posts_without_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_without_authentication(self):
        data = {'image': 'new_image.jpg', 'caption': 'new caption'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_with_invalid_data(self):
        self.client.force_authenticate(user=self.user1)
        data = {'image': 'new_image.jpg'}  # missing caption
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PostDetailAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        self.post1 = Post.objects.create(user=self.user1, image='image1.jpg', caption='caption1')
        self.post2 = Post.objects.create(user=self.user2, image='image2.jpg', caption='caption2')

    def test_get_post(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-detail', kwargs={'post_id': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post1.id)

    def test_get_post_without_authentication(self):
        url = reverse('post-detail', kwargs={'post_id': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post_with_invalid_id(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-detail', kwargs={'post_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-detail', kwargs={'post_id': self.post1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_without_authentication(self):
        url = reverse('post-detail', kwargs={'post_id': self.post1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_with_invalid_id(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('post-detail', kwargs={'post_id': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LikeToggleAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        self.post1 = Post.objects.create(user=self.user1, image='image1.jpg', caption='caption1')

    def test_like_post(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('like', kwargs={'post_id': self.post1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post1.likes.count(), 1)

    def test_unlike_post(self):
        Like.objects.create(user=self.user2, post=self.post1)
        self.client.force_authenticate(user=self.user2)
        url = reverse('like', kwargs={'post_id': self.post1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post1.likes.count(), 0)

    def test_like_post_without_authentication(self):
        url = reverse('like', kwargs={'post_id': self.post1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_post_with_invalid_id(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('like', kwargs={'post_id': 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CommentListCreateAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password', email='user2@example.com')
        self.post1 = Post.objects.create(user=self.user1, image='image1.jpg', caption='caption1')

    def test_create_comment_without_authentication(self):
        url = reverse('comments', kwargs={'post_id': self.post1.id})
        data = {'content': 'This is a comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_with_invalid_id(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('comments', kwargs={'post_id': 9999})
        data = {'content': 'This is a comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_comments(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('comments', kwargs={'post_id': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_comments_without_authentication(self):
        url = reverse('comments', kwargs={'post_id': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
