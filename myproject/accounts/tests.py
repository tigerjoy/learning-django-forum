from django.test import TestCase
from django.urls import resolve, reverse

from .views import signup

# Create your tests here.
class SignUpTests(TestCase):
    # Checks if the signup/ route is functioning 
    # and serving a HTML or not
    def test_signup_status_code(self):
        signup_url = reverse("signup")
        response = self.client.get(signup_url)
        self.assertEquals(response.status_code, 200)

    # Checks if /signup/ url resolves to a correct view
    def test_signup_url_resolves_to_signup_view(self):
        view = resolve("/signup/")
        self.assertEquals(view.func, signup)