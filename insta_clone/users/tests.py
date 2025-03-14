from django.test import TestCase

from users.models import User  


class UserModelTest(TestCase):

    def setUp(self):
        """Create test users."""
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password123"
        )

    def test_create_user(self):
        """Test user creation with valid data."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass"))

    def test_username_unique(self):
        """Ensure username must be unique."""
        with self.assertRaises(Exception):  
            User.objects.create(username="user1", email="duplicate@example.com", password="password123")

    def test_email_unique(self):
        """Ensure email must be unique."""
        with self.assertRaises(Exception):  
            User.objects.create(username="uniqueuser", email="user1@example.com", password="password123")

    def test_followers_relationship(self):
        """Test the ManyToManyField relationship (followers)."""
        self.user1.followers.add(self.user2)  
        self.assertIn(self.user2, self.user1.followers.all())
        self.assertIn(self.user1, self.user2.following.all())

    def test_profile_picture_upload(self):
        """Ensure profile picture can be blank/null."""
        user = User.objects.create(username="test_pic", email="pic@example.com", password="password123")
        self.assertFalse(bool(user.profile_picture))

    def test_password_encryption(self):
        """Ensure password is hashed and not stored in plain text."""
        self.assertNotEqual(self.user1.password, "password123") 
        self.assertTrue(self.user1.check_password("password123"))  

