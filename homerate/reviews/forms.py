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

    def __init__(self, *args, **kwargs):
        super(HouseReportForm, self).__init__(*args, **kwargs)
        self.fields['repair_quality'].required = False
        self.fields['furniture_quality'].required = False
        self.fields['mattress_quality'].required = False
        self.fields['build_quality'].required = False
        self.fields['smells'].required = False
        self.fields['damp_mould_free'].required = False
        self.fields['image'].required = False


