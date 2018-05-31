from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import HouseForm, HouseReportForm
from .models import House
from .models import HouseReport
# Create your views here.


def house(request, id):
    # Query database for house with correct id
    houses = House.objects.filter(id=id)

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
    houses = House.objects.filter(id=id)

    # Check house exists
    if len(houses) == 0:
        return render(request, 'reviews/nohouse.html', {})
    house = houses[0]

    print(id)
    print(house)

    if(request.method == "POST"):
        print("post")
        print(request.POST)
        form = HouseReportForm(request.POST)
        print(form)
        if(form.is_valid()):
            print("valid")
            report = form.save(commit=False)
            report.house_filed = house
            report.save()
            print(report)
            return redirect('house', id=house.id)
        else:
            print("Form Error")
            print(form.errors)
    form = HouseReportForm()
    return render(request, 'reviews/newreport.html', {'new_report_form' : form, 'house' : house})


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
    form = HouseForm()
    return render(request, 'reviews/newhouse.html', {'new_house_form' : form})