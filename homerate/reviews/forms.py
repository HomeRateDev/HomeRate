from django import forms

from .models import House, HouseReport


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ('address',)


class HouseDetailsForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ['address', 'date_created']


class HouseReportForm(forms.ModelForm):
    class Meta:
        model = HouseReport
        exclude = ['house_filed', 'author']
