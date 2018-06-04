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

    landlord_responsiveness_weight = 2
    repair_quality_weight = 2

    water_pressure_weight = 1
    utilities_weight = 1
    furniture_quality_weight = 1
    mattress_quality_weight = 1
    build_quality_weight = 1

    quietness_weight = 1
    pest_free_weight = 2
    smells_weight = 1
    damp_mould_free_weight = 2

    def star_rating(self):
        reports = HouseReport.objects.filter(house_filed=self).order_by('-moved_out_date')
        time_dependant_rating_weight = 1
        time_dependant_rating_weight_total = 0
        total_report_rating = 0
        if len(reports) == 0:
            return None
        for report in reports:
            total_report_rating += report.get_general_rating() * time_dependant_rating_weight
            time_dependant_rating_weight_total += time_dependant_rating_weight
            time_dependant_rating_weight = time_dependant_rating_weight * 0.6

        total_report_rating = total_report_rating / time_dependant_rating_weight_total
        return round(total_report_rating*100)/100





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

    general_rating = None

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.house_filed) + " - " + str(self.author) + " - " + str(self.moved_in_date)

    def get_general_rating(self):
        total_report_weight = 0
        rating = 0
        if hasattr(self, 'landlord_responsiveness'):
            rating += self.landlord_responsiveness * House.landlord_responsiveness_weight
            total_report_weight += House.landlord_responsiveness_weight
        if hasattr(self, 'repare_quality'):
            rating += self.repare_quality * House.repair_quality_weight
            total_report_weight += House.repair_quality_weight
        if hasattr(self, 'water_pressure'):
            rating += self.water_pressure * House.water_pressure_weight
            total_report_weight += House.water_pressure_weight
        if hasattr(self, 'utilities'):
            rating += self.utilities * House.utilities_weight
            total_report_weight += House.utilities_weight
        if hasattr(self, 'furniture_quality'):
            rating += self.furniture_quality * House.furniture_quality_weight
            total_report_weight += House.furniture_quality_weight
        if hasattr(self, 'mattress_quality'):
            rating += self.mattress_quality * House.mattress_quality_weight
            total_report_weight += House.mattress_quality_weight
        if hasattr(self, 'build_quality'):
            rating += self.build_quality * House.build_quality_weight
            total_report_weight += House.build_quality_weight
        if hasattr(self, 'quietness'):
            rating += self.quietness * House.quietness_weight
            total_report_weight += House.quietness_weight
        if hasattr(self, 'pest_free'):
            rating += self.pest_free * House.pest_free_weight
            total_report_weight += House.pest_free_weight
        if hasattr(self, 'smells'):
            rating += self.smells * House.smells_weight
            total_report_weight += House.smells_weight
        if hasattr(self, 'damp_mould_free'):
            rating += self.damp_mould_free * House.damp_mould_free_weight
            total_report_weight += House.damp_mould_free_weight
        rating = rating / total_report_weight
        self.general_rating = round(rating*10)/10
        return rating
