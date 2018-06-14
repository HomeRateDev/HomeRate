from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='account.activate'),
    url(r'delete$', views.delete_account, name='delete_account'),
    url(r'sign-up$', views.sign_up, name='sign-up'),
    url(r'login$', auth_views.login, name='login'),
    url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'$', views.profile, name='profile'),
]
