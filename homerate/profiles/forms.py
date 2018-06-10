from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        label_suffix='',
        widget=forms.EmailInput(attrs={
            'pattern': "^[\w!#$%&'*+\/=?^`{|}~-]+(?:\.[\w!#$%&'*+\/=?`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+(?:ac\.uk)$",
            'oninvalid': "setCustomValidity('You must use a .ac.uk email to sign up for HomeRate')"
        })
    )
    first_name = forms.CharField(max_length=20, label_suffix='')
    password1 = forms.CharField(widget=forms.PasswordInput(), label_suffix='', label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label_suffix='', label='Password Confirmation')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'password1', 'password2')
