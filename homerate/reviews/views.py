from django.shortcuts import render
from django.utils import timezone

from .forms import HouseForm
from .models import House
from .models import HouseReport
# Create your views here.


def house(request, number):
    print(number)
    house = House.objects.filter(id=number)
    print(house)
    if len(house) == 0:
        return render(request, 'reviews/nohouse.html', {})

    reviews = HouseReport.objects.filter(house_filed = house[0])
    print(reviews)
    print(house[0])
    return render(request, 'reviews/house.html', {'house' : house[0], 'reviews' : reviews})


def new_house(request):
    if(request.method == "POST"):
        form = HouseForm(request.POST)
        print("POST")
        print(request.POST)
        print("FORM")
        print(form)
        if(form.is_valid()):
            house = form.save(commit=False)
            house.date_created = timezone.now()
            house.save()
            print(house.id)

    else:
        form = HouseForm()
    return render(request, 'reviews/newhouse.html', {'new_house_form' : form})