from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from model_bakery import baker


class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = baker.make(User)
        self.user.set_password('testpass123')
        self.user.save()

    def test_register_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_post_success(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_post_password_mismatch(self):
        data = {
            'username': 'newuser',
            'password': 'pass123',
            'password2': 'different'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")

    def test_login_get(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_post_success(self):
        data = {'username': self.user.username, 'password': 'testpass123'}
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:book_list'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_post_invalid_credentials(self):
        data = {'username': 'wrong', 'password': 'wrong'}
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_login_with_next_parameter(self):
        next_url = reverse('books:my_books')
        login_url = f"{reverse('accounts:login')}?next={next_url}"
        data = {'username': self.user.username, 'password': 'testpass123'}
        response = self.client.post(login_url, data)
        self.assertRedirects(response, next_url)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('books:book_list'))
        self.assertNotIn('_auth_user_id', self.client.session)
