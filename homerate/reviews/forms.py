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

    def __init__(self, *args, **kwargs):
        super(HouseDetailsForm, self).__init__(*args, **kwargs)

        room_range = {'min': 0, 'max': 100}

        self.fields['bedrooms'].required = True
        self.fields['bedrooms'].widget = forms.NumberInput(
            attrs=room_range
        )

        self.fields['bathrooms'].required = True
        self.fields['bathrooms'].widget = forms.NumberInput(
            attrs=room_range
        )

        self.fields['living_rooms'].required = True
        self.fields['living_rooms'].widget = forms.NumberInput(
            attrs=room_range
        )


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
        self.fields['moved_in_date'].widget = forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',
                'data-toggle': 'datepicker'
            }
        )
        self.fields['moved_out_date'].widget = forms.TextInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',
                'data-toggle': 'datepicker'
            }
        )
        self.fields['landlord_comment'].widget = forms.Textarea(
            attrs={
                'placeholder': 'Add your comment about the landlord...'
            }
        )
        self.fields['construction_quality_comment'].widget = forms.Textarea(
            attrs={
                'placeholder': "Add your comment about the house's construction quality..."
            }
        )
        self.fields['nuisances_comment'].widget = forms.Textarea(
            attrs={
                'placeholder': 'Add your comment about any nuisances in the property...'
            }
        )
        self.fields['affordability_comment'].widget = forms.Textarea(
            attrs={
                'placeholder': "Add your comment about the house's affordability..."
            }
        )

    def is_valid(self):
        self.fields['landlord_responsiveness'].required = True
        self.fields['water_pressure'].required = True
        self.fields['utilities'].required = True
        self.fields['quietness'].required = True
        self.fields['pest_free'].required = True

        valid =  super(HouseReportForm, self).is_valid()

        self.fields['landlord_responsiveness'].required = False
        self.fields['water_pressure'].required = False
        self.fields['utilities'].required = False
        self.fields['quietness'].required = False
        self.fields['pest_free'].required = False

        return valid



