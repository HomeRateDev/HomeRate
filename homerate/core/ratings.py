from django import forms
from django.db import models


class RatingField(models.CharField):
    description = ""


    def __init__(self, mandatory=False, weighting=False, *args, min_rating = 1,
                 max_rating = 5, **kwargs):
        if weighting:
            self.description = "A weighting from " + str(min_rating) + " to " + str(max_rating)
        else:
            self.description = "A star rating from " + str(min_rating) + " to " + str(max_rating)

        self.mandatory = mandatory
        self.weighting = weighting

        self.choices = [(str(i), i) for i in range(min_rating, max_rating + 1)]
        if not self.mandatory:
            self.choices = [("", 0)] + self.choices
            kwargs['blank'] = True
            kwargs['null'] = True
        else:
            if not 'default' in kwargs:
                kwargs['default'] = (max_rating + min_rating) / 2

        kwargs['choices'] = self.choices
        kwargs['max_length'] = len(str(max_rating))
        super().__init__(*args, **kwargs)


    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.mandatory:
            kwargs['mandatory'] = self.mandatory
        return name, path, args, kwargs


    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        kwargs['choices'] = self.choices

        if self.weighting:
            class_string = "weighting"
        else:
            class_string = "starRating"

        if self.mandatory:
            class_string += "Mandatory"

        return forms.ChoiceField(widget=forms.Select(attrs={'class': class_string}), **kwargs)

