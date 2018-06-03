# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.db import models
from django.utils import timezone

# Create your models here.


class RatingField(models.IntegerField):

    description = "A star rating from 1 to 5"
    min_rating = 1
    max_rating = 5
    choices = [(i, i) for i in range(min_rating, max_rating + 1)]

    def __init__(self, mandatory=False, *args, **kwargs):
        self.mandatory = mandatory
        kwargs['choices'] = self.choices
        if not self.mandatory:
            kwargs['null'] = True
        else:
            kwargs['default'] = (self.max_rating + self.min_rating) / 2
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.mandatory:
            kwargs['mandatory'] = self.mandatory
        return name, path, args, kwargs

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        kwargs['choices'] = self.choices
        return forms.ChoiceField(**kwargs)


class House(models.Model):
    address = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    living_rooms = models.IntegerField(default=0)

    def __str__(self):
        return self.address


class HouseReport(models.Model):

    # Basic Info
    house_filed = models.ForeignKey('reviews.House', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    moved_in_date = models.DateField(blank=True, null=True)
    moved_out_date = models.DateField(blank=True, null=True)

    # Landlord
    landlord_responsiveness = RatingField(mandatory=True)
    repair_quality = RatingField()

    # Construction Quality
    water_pressure = RatingField(mandatory=True)
    utilities = RatingField(mandatory=True)
    furniture_quality = RatingField()
    mattress_quality = RatingField()
    build_quality = RatingField()

    # Nuisances
    quietness = RatingField(mandatory=True)
    pest_free = RatingField(mandatory=True)
    smells = RatingField()
    damp_mould_free = RatingField()

    # Affordability
    monthly_rent = models.IntegerField(default=0)
    monthly_bills = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.house_filed) + " - " + str(self.author) + " - " + str(self.moved_in_date)