from django import forms

from .models import House, HouseReport


class HouseForm(forms.ModelForm):

    class Meta:
        model = House
        fields = ('addr',)


class HouseReportForm(forms.ModelForm):

    class Meta:
        model = HouseReport
        fields = ('author',
                  'moved_in_date',
                  'description',
                  'pros',
                  'cons',
                  'monthly_cost',)