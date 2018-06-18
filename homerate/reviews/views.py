from urllib.parse import unquote

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from requests import auth

from profiles.forms import CommutePostcode
from profiles.models import Profile
from reviews.imageSafeSearch import is_adult_content
from .forms import HouseForm, HouseReportForm, HouseDetailsForm
from .models import House, HouseReport, ReviewImage
# Create your views here.

@login_required
def flag_report(request, id):
    report = HouseReport.objects.get(pk=id)
    report.reported_by.add(request.user)
    return redirect('house', id)


@login_required
def unflag_report(request, id):
    report = HouseReport.objects.get(pk=id)
    report.reported_by.remove(request.user)
    return redirect('house', id)

@login_required
def save_house(request, id):
    house = get_object_or_404(House, pk=id)
    profile = Profile.objects.get(user=request.user)
    profile.saved_houses.add(house)
    return redirect('house', id=id)

@login_required
def unsave_house(request, id):
    house = get_object_or_404(House, pk=id)
    profile = Profile.objects.get(user=request.user)
    profile.saved_houses.remove(house)
    return redirect('house', id=id)

def house(request, id):
    user_profile = Profile.objects.get(user=request.user) if request.user.is_authenticated else None
    # Query database for house with correct id
    houses = House.objects.filter(id=id)

    # If no house found return a no house page
    # TODO make this it's own view and redirect instead
    if len(houses) == 0:
        return render(request, 'reviews/nohouse.html', {})

    house = houses[0]
    reviews = HouseReport.objects.filter(house_filed=house).filter(visible=True).order_by('-moved_out_date')
    aggregate = HouseReport.make_aggregate(reviews)
    flagged_reports = set()

    if request.user.is_authenticated:
        for review in reviews:
            if review.reported_by.filter(username=request.user.username).exists():
                flagged_reports.add(review.pk)

        print(flagged_reports)

        user_saved = house in user_profile.saved_houses.all()

        # Create an empty list for the images
        images = []
        for report in reviews:
            # Calculate the general rating
            report.get_personal_rating(user_profile)
            # Append the images in to the list
            images += ReviewImage.objects.filter(house_report=report)
        rating = house.personal_star_rating(user_profile)
    else:
        rating = house.general_star_rating()
        reviews = None
        images = None
        user_saved = None


    # Construct a split-up version of the address
    address_components = house.split_address()

    postcode_form = None
    profilepostcode = None
    if request.user.is_authenticated:
        postcode_form = CommutePostcode(instance=Profile.objects.get(user=request.user))
        profilepostcode = user_profile.getPostcode()

    if profilepostcode is not None:
        profilepostcode = profilepostcode.upper()

    # return house view page with house and list of reports
    return render(
        request, 'reviews/house.html', {
            'house': house,
            'reviews': reviews,
            'rating': rating,
            'images': images,
            'address_components': address_components,
            'profilepostcode': profilepostcode,
            'postcodeForm': postcode_form,
            'user_saved' : user_saved,
            'aggregate': aggregate,
            'flagged_reports': flagged_reports,
        }
    )
        
        

@login_required
def new_report(request, id):
    # Create a formset factory for multiple images
    image_formset_factory = modelformset_factory(ReviewImage, fields=('image',), extra=4)

    # Get relevant house
    houses = House.objects.filter(id=id)

    # Check house exists
    if len(houses) == 0:
        return render(request, 'reviews/nohouse.html', {})
    house = houses[0]

    # Check a POST request has been received
    if request.method == "POST":

        house_details_form = HouseDetailsForm(request.POST, instance=house)
        review_form = HouseReportForm(request.POST, request.FILES)
        image_formset = image_formset_factory(request.POST, request.FILES)

        # Ensure both forms are valid
        if house_details_form.is_valid() and review_form.is_valid() and image_formset.is_valid():

            # Prepare to save review, but don't commit to database yet
            report = review_form.save(commit=False)

            # Insert foreign key from House model
            report.house_filed = house

            report.author = request.user

            if Profile.objects.get(user=request.user).is_suspicious:
                report.visible = False
            else:
                report.visible = True

            # Commit review to database
            report.save()
            house_details_form.save()

            # By default profiles don't need review
            needs_review = False

            for img in image_formset:
                try:
                    # Save the reviews to the database
                    photo = ReviewImage(house_report=report, image=img.cleaned_data['image'])
                    photo.save()

                    # If the image is adult content then delete the file, remove the database entry
                    if is_adult_content(photo.image.url):
                        # Delete the image from the database
                        ReviewImage.objects.get(pk=photo.pk).delete()

                        # Flag for review and nake the report no longer visible
                        needs_review = True
                        report.visible = False
                        report.save(update_fields=["visible"])

                except Exception as e:
                    # Users may not insert photos in order. Try remaining photos.
                    continue

            # If needs a manual review then render a warning
            if needs_review :
                return render(request, 'reviews/suspicious_report.html', {'id': house.pk})

            return redirect('house', id=house.id)
        else:
            print("Form Error")
            print(review_form.errors)
            print(house_details_form.errors)
            print(image_formset.errors)

    house_details_form = HouseDetailsForm(instance=house)
    review_form = HouseReportForm()
    image_formset = image_formset_factory(queryset=ReviewImage.objects.none())

    return render(request, 'reviews/newreport.html', {
                      'house_details_form': house_details_form,
                      'new_report_form': review_form,
                      'house': house,
                      'image_formset': image_formset,
                      'is_suspicious': Profile.objects.get(user=request.user).is_suspicious
                  })


@login_required
def edit_report(request, id):
    report = get_object_or_404(HouseReport, pk=id)
    house = report.house_filed

    if request.method == "POST":
        house_details_form = HouseDetailsForm(request.POST, instance=house)
        review_form = HouseReportForm(request.POST, request.FILES, instance=report)

        # Ensure both forms are valid
        if house_details_form.is_valid() and review_form.is_valid():

            # Prepare to save review, but don't commit to database yet
            report = review_form.save(commit=False)

            # Insert foreign key from House model
            report.house_filed = house

            if Profile.objects.get(user=request.user).is_suspicious:
                report.visible = False
            else:
                report.visible = True

            # Save house details
            house_details_form.save()

            report.author = request.user

            # Commit review to database
            report.save()

            return redirect('house', id=house.id)
        else:
            print("Form Error")
            print(review_form.errors)
    else:
        house_details_form = HouseDetailsForm(instance=house)
        review_form = HouseReportForm(instance=report)

        return render(request, 'reviews/newreport.html', {
            'house_details_form': house_details_form,
            'new_report_form': review_form,
            'house': house,
            'edit_page': True,
            'is_suspicious': Profile.objects.get(user=request.user).is_suspicious
        })

@login_required
def delete_report(request, id):
    report = get_object_or_404(HouseReport, pk=id)
    house = report.house_filed
    report.delete()
    return redirect('house', id=house.id)


def check_house(request, encoded_addr):
    # Decode the address
    address_str = unquote(encoded_addr)

    # Query the database to check if the house already exists
    query = House.objects.filter(address=address_str)

    if query.count() > 0:
        # The house exists, redirect to it
        return redirect('house', id=query.first().id)
    else:
        # The house doesn't exist, create a new house
        new_house_entry = House(address=str(address_str))
        new_house_entry.save()
        return redirect('house', id=new_house_entry.id)
