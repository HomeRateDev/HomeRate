from django.shortcuts import render

from .forms import HouseForm
from .models import House
from .models import HouseReport
# Create your views here.


def house(request, number):
    print(number)
    house = House.objects.filter(house_id=number)
    print(house)
    if len(house) == 0:
        return render(request, 'reviews/nohouse.html', {})

    reviews = HouseReport.objects.filter(house_filed = house[0])
    print(reviews)
    print(reviews[0].moved_in_date)
    print(house[0])
    return render(request, 'reviews/house.html', {'house' : house[0], 'reviews' : reviews})


def new_house(request):
    form = HouseForm()
    return render(request, 'reviews/newhouse.html', {'new_house_form' : form})