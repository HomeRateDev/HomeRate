from django import forms
from django.forms import NumberInput

from .models import House, HouseReport


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ('address',)


class HouseReportForm(forms.ModelForm):
    class Meta:
        model = HouseReport
        exclude = ['house_filed']
