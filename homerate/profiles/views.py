from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.forms import SignupForm, StarRatingWeighting

from profiles.tokens import account_activation_token

import os

from .models import Profile


def sign_up(request):
    if request.user.is_authenticated:
        return render(request, 'registration/already_signed_in.html')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                if user.email[-6:] != ".ac.uk":
                    return render(request, 'registration/signup_error.html')
                user.username = user.email
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate your HomeRate account.'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return render(request, 'registration/please_activate.html')
        else:
            form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        new_profile = Profile()
        new_profile.user = user
        new_profile.email_confirmed = True
        new_profile.save()
        login(request, user)
        return render(request, 'registration/activation_successful.html')
    else:
        return render(request, 'registration/activation_unsuccessful.html')

def account_activation_sent(request):
    return render(request, 'registration/please_activate.html')

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = StarRatingWeighting(request.POST, instance=Profile.objects.get(user=request.user))
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
            else:
                print("Form Error")
                print(form.errors)

        else:
            form = StarRatingWeighting(instance=Profile.objects.get(user=request.user))

        return render(request, 'profiles/profile.html', {'form': form})
    else:
        return render(request, 'profiles/signin_to_view.html')
