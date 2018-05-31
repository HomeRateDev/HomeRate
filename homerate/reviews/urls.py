from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(\d+)', views.house, name='house'),
    url(r'new_house', views.new_house, name='new_house'),
]