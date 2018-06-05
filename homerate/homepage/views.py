from django.shortcuts import render
from reviews.models import House


# Create your views here.
def homepage(request):
    houses = House.objects.order_by('-date_created')
    return render(request, 'homepage/homepage.html', {'houses': houses})
