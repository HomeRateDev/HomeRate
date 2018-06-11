from django import forms
from django.db import models


class RatingField(models.CharField):

    description = "A star rating from 1 to 5"
    min_rating = 1
    max_rating = 5

    def __init__(self, mandatory=False, weighting=False, *args, **kwargs):
        if weighting:
            self.description = "A weighting from 1 to 5"
        else:
            self.description = "A star rating from 1 to 5"

        self.mandatory = mandatory
        self.weighting = weighting

        self.choices = [(str(i), i) for i in range(self.min_rating, self.max_rating + 1)]
        if not self.mandatory:
            self.choices = [("", 0)] + self.choices
        else:
            kwargs['default'] = (self.max_rating + self.min_rating) / 2

        kwargs['choices'] = self.choices
        kwargs['blank'] = True
        kwargs['null'] = True
        kwargs['max_length'] = 1
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.mandatory:
            kwargs['mandatory'] = self.mandatory
        return name, path, args, kwargs

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        kwargs['choices'] = self.choices
        class_string = "starRating"
        if self.mandatory:
            class_string += "Mandatory"
        return forms.ChoiceField(widget=forms.Select(attrs={'class': class_string}), **kwargs)