from django.core.checks import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from profiles.forms import SignupForm, StarRatingWeighting, CommutePostcode, FirstNameChange

from profiles.tokens import account_activation_token

import os

from reviews.models import House, HouseReport
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
                if User.objects.filter(username=user.username).exists():
                    return render(request, 'registration/username_exists.html', {'username': user.username})
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate your HomeRate account.'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('utf-8'),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return render(request, 'registration/please_activate.html')
        else:
            form = SignupForm()

        reqs = [
            {'text': '8 characters minimum', 'name': 'length'},
            {'text': 'Not entirely numeric', 'name': 'numeric'}
        ]
        return render(request, 'registration/signup.html', {'form': form, 'passwordReqs': reqs})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        profile = Profile.objects.get(user=user)
        profile.email_confirmed = True
        profile.save()
        login(request, user)
        return render(request, 'registration/activation_successful.html')
    else:
        return render(request, 'registration/activation_unsuccessful.html')

def account_activation_sent(request):
    return render(request, 'registration/please_activate.html')

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            weights_form = StarRatingWeighting(request.POST, instance=Profile.objects.get(user=request.user))
            postcode_form = CommutePostcode(request.POST, instance=Profile.objects.get(user=request.user))
            first_name_form = FirstNameChange(request.POST, instance=request.user)

            if weights_form.is_valid():
                profile = weights_form.save(commit=False)
                profile.user = request.user
                profile.save()
            elif postcode_form.is_valid():
                profile = postcode_form.save(commit=False)
                profile.save(update_fields=["postcode"])
            else:
                print("Form Error")
                print(weights_form.errors)

            if first_name_form.is_valid():
                form = first_name_form.save(commit=False)
                form.save(update_fields=["first_name"])


        weights_form = StarRatingWeighting(instance=Profile.objects.get(user=request.user))
        postcode_form = CommutePostcode(instance=Profile.objects.get(user=request.user))
        saved_houses = Profile.objects.get(user=request.user).saved_houses.all()
        reports = HouseReport.objects.filter(author=request.user)

        for house in saved_houses:
            house.personal_star_rating(Profile.objects.get(user=request.user))

        first_name_form = FirstNameChange(instance=request.user)

        return render(request, 'profiles/profile.html', {
            'reports': reports,
            'saved_houses': saved_houses,
            'weights_form': weights_form,
            'postcode_form':postcode_form,
            'first_name_form': first_name_form
        })
    else:
        return render(request, 'profiles/signin_to_view.html')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })