from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        # Regex to match UK postcodes
        r'postcode/(?P<postcode>(GIR ?0AA|[A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]([0-9ABEHMNPRV-Y])?)|[0-9][A-HJKPS-UW]) ?[0-9][ABD-HJLNP-UW-Z]{2}))/$',
        views.api_request,
        name='address_api')
]
