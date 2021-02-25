from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.urls import resolve, reverse

from .views import signup

# Create your tests here.
class SignUpTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.get(url)
        
    # Checks if the signup/ route is functioning 
    # and serving a HTML or not
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # Checks if /signup/ url resolves to a correct view
    def test_signup_url_resolves_to_signup_view(self):
        view = resolve("/signup/")
        self.assertEquals(view.func, signup)
    
    # Checks to see if the Sign Up form contains the csrf token
    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")
    
    # Checks to see if the Sign Up form is present in the 
    # signup() view or not
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, UserCreationForm)
    
class SuccessfulSignUpTests(TestCase):
    # Set up mock data
    def setUp(self):
        url = reverse('signup')
        data = {
            "username": "john",
            "password1": "abcdef123456",
            "password2": "abcdef123456"
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
    
    # Checks if on successful sign up, if the view successfully
    # redirects back to the homepage
    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the home page
        '''
        self.assertRedirects(self.response, self.home_url)
    
    # Checks if the successful form submission created a new user
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())
    
    # Checks to see if the user in the context of the home page
    # is authenticated
    def test_user_authentication(self):
        '''
        Create a new request to an arbitary page.
        The resulting response should now have a user to its context
        after a successful signup.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)




