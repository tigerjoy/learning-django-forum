from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=254, 
        required=True, 
        widget=forms.EmailInput(),
        help_text='''
        <ul>
            <li>Your email id a required field.</li>
            <li>Your email id will be required for resetting of password later.</li>
        </ul>
        '''
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")