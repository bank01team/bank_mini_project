from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2')