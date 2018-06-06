from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'sign-up$', views.sign_up, name='sign-up'),
    url(r'login$', auth_views.login, name='login'),
    url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'$', views.profile, name='profile'),
]