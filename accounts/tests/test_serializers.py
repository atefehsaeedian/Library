from django.test import TestCase
from django.contrib.auth.models import User
from model_bakery import baker
from accounts.serializers import RegisterSerializer, LoginSerializer


class AccountsSerializersTest(TestCase):

    def test_register_serializer_valid_data(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'password2': 'strongpass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('strongpass123'))

    def test_register_serializer_passwords_dont_match(self):
        data = {
            'username': 'newuser',
            'password': 'pass123',
            'password2': 'different123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Passwords do not match!', str(serializer.errors))

    def test_register_serializer_username_exists(self):
        baker.make(User, username='existing')
        data = {
            'username': 'existing',
            'password': 'pass123',
            'password2': 'pass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('A user with that username already exists.', str(serializer.errors))

    def test_login_serializer_valid_credentials(self):
        user = baker.make(User, username='testuser')
        user.set_password('testpass123')
        user.save()

        data = {'username': 'testuser', 'password': 'testpass123'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, user)

    def test_login_serializer_invalid_credentials(self):
        data = {'username': 'wronguser', 'password': 'wrongpass'}
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid username or password.', str(serializer.errors))