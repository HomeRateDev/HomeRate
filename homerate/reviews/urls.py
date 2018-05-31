from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<id>\d+)$', views.house, name='house'),
    url(r'new_report/(?P<id>\d+)/$', views.new_report, name='new_report'),
    url(r'new_house$', views.new_house, name='new_house'),
]