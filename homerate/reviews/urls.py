from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'house/(?P<id>\d+)$', views.house, name='house'),
    url(r'new_report/(?P<id>\d+)/$', views.new_report, name='new_report'),
    url(r'edit_report/(?P<id>\d+)/$', views.edit_report, name='edit_report'),
    url(r'delete_report/(?P<id>\d+)/$', views.delete_report, name='delete_report'),
    url(r'new_house$', views.new_house, name='new_house'),
    url(r'check_address/(?P<encoded_addr>.*$)', views.check_house, name='check_house'),
]