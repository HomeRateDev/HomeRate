# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import NumberInput, forms
from django.utils import timezone

# Create your models here.


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class RatingField(IntegerRangeField):
    def __init__(self, verbose_name=None, name=None, mandatory=False, **kwargs):
        self.mandatory = mandatory
        min_rating, max_rating, default_rating = 1, 5, 3
        if mandatory:
            IntegerRangeField.__init__(self, verbose_name, name, min_rating, max_rating, default=default_rating)
        else:
            IntegerRangeField.__init__(self,
                                       verbose_name,
                                       name,
                                       min_rating, max_rating,
                                       default=default_rating,
                                       blank=True,
                                       null=True
                                       )

    def formfield(self, **kwargs):
        defaults = {'widget': NumberInput(attrs={'type': 'range'})}
        defaults.update(**kwargs)
        return super().formfield(**defaults)


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