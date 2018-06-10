import os

from django.http import HttpResponse
import requests


# Create your views here.
def api_request(request, postcode):
    url = 'https://api.getAddress.io/find/' + postcode
    r = requests.get(url, params={
        'api-key': os.environ['ADDRESS_IO_API_KEY']
    })
    return HttpResponse(r.text, content_type='application/json')
