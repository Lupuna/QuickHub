from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views
from q_registration import views as q_registration_views


class TestUrls(SimpleTestCase):

    def test_sing_up_url_is_resolve(self):
        url = reverse('registration:sign_up')
        self.assertEqual(resolve(url).func, q_registration_views.sign_up)

    def test_sing_in_url_is_resolve(self):
        url = reverse('registration:login')
        self.assertEqual(resolve(url).func.view_class, q_registration_views.LoginCustom)

    def test_logout_url_is_resolve(self):
        url = reverse('registration:logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

    def test_password_reset_url_is_resolve(self):
        url = reverse('registration:password_reset')
        self.assertEqual(resolve(url).func.view_class, q_registration_views.PasswordResetViewCustom)

    def test_password_reset_done_url_is_resolve(self):
        url = reverse('registration:password_reset_done')
        self.assertEqual(resolve(url).func.view_class, q_registration_views.PasswordResetDoneViewCustom)
