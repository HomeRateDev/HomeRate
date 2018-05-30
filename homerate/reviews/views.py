from django.shortcuts import render

from .models import House
from .models import HouseReport
# Create your views here.

def house(request, number):
    print(number)
    house = House.objects.filter(house_id=number)
    print(house)
    if len(house) == 0:
        return render(request, 'reviews/nohouse.html', {})

    print(house[0])
    return render(request, 'reviews/house.html', {'house' : house[0]})