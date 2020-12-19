from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@gmAil.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='1234'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test the email for a new user is null"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password='1234')

    def test_new_user_create_superuser(self):
        """Test to create a super user"""
        user = get_user_model().objects.create_superuser(
            'test_superuser@gmail.com',
            'test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
