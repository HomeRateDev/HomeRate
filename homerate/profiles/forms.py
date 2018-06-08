from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required', label_suffix='')
    first_name = forms.EmailField(max_length=20, label_suffix='')
    password1 = forms.CharField(widget=forms.PasswordInput(), label_suffix='', label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label_suffix='', label='Password Confirmation')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')
