from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import HouseForm
from .models import House
from .models import HouseReport
# Create your views here.


def house(request, number):
    # Query database for house with correct id
    houses = House.objects.filter(id=number)

    # If no house found return a no house page
    # TODO make this it's own view and redirect instead
    if len(houses) == 0:
        return render(request, 'reviews/nohouse.html', {})

    house = houses[0]
    # Query database for reports about the house.
    reviews = HouseReport.objects.filter(house_filed = house)

    # return house view page with house and list of reports
    return render(request, 'reviews/house.html', {'house' : house, 'reviews' : reviews})


def new_report(request, id):
    # Get relevant house
    house = House.objects.filter(id=id)

    # Check house exists
    if len(house) == 0:
        return render(request, 'reviews/nohouse.html', {})

    return render(request, 'reviews/house.html', {'house' : house[0]})


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

        return redirect('new_report', id=house.id)

    else:
        form = HouseForm()
        return render(request, 'reviews/newhouse.html', {'new_house_form' : form})