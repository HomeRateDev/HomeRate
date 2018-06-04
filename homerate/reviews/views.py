from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import HouseForm, HouseReportForm, HouseDetailsForm
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
    reviews = HouseReport.objects.filter(house_filed = house).order_by('-moved_out_date')
    for report in reviews:
        report.get_general_rating()
    rating = house.star_rating()

    # return house view page with house and list of reports
    return render(request, 'reviews/house.html', {'house' : house, 'reviews' : reviews, 'rating':rating})


def new_report(request, id):
    # Get relevant house
    houses = House.objects.filter(id=id)

    # Check house exists
    if len(houses) == 0:
        return render(request, 'reviews/nohouse.html', {})
    house = houses[0]

    # Check a POST request has been received
    if request.method == "POST":
        house_details_form = HouseDetailsForm(request.POST)
        review_form = HouseReportForm(request.POST)

        # Ensure both forms are valid
        if house_details_form.is_valid() and review_form.is_valid():

            # Prepare to save review, but don't commit to database yet
            report = review_form.save(commit=False)

            # Insert foreign key from House model
            report.house_filed = house

            # Save house details
            house_details_form.save()

            # Commit review to database
            report.save()

            return redirect('house', id=house.id)
        else:
            print("Form Error")
            print(review_form.errors)

    house_details_form = HouseDetailsForm()
    review_form = HouseReportForm()

    return render(request, 'reviews/newreport.html', {
                      'house_details_form': house_details_form,
                      'new_report_form': review_form,
                      'house': house,
                  })


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