from django.test import TestCase
from django.urls import reverse, resolve
from accounts import views


class AccountsURLsTest(TestCase):
    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, views.RegisterView)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, views.LoginView)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, views.LogoutView)