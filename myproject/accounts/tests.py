from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from .views import signup
from .forms import SignUpForm

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
        self.assertIsInstance(form, SignUpForm)
    
    def test_form_input(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)
    
class SuccessfulSignUpTests(TestCase):
    # Set up mock data
    def setUp(self):
        url = reverse('signup')
        data = {
            "username": "john",
            "password1": "abcdefgh12345",
            "password2": "abcdefgh12345",
            "email": "john@doe.com"
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

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        # Submit an empty dictionary
        self.response = self.client.post(url, {})

    # Checks if the sign up page upon submitting invalid data
    # returns to the same page
    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEqual(self.response.status_code, 200)

    # Checks if the form after submission contains errors
    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)
    
    # Checks if an user has been created after submission of 
    # erroneous form
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

