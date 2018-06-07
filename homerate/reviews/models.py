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

    def __init__(self, mandatory=False, *args, **kwargs):
        self.mandatory = mandatory
        self.choices = [(i, i) for i in range(self.min_rating, self.max_rating + 1)]
        if not self.mandatory:
            kwargs['null'] = True
            self.choices = [(None, 0)] + self.choices
        else:
            kwargs['default'] = (self.max_rating + self.min_rating) / 2
        kwargs['choices'] = self.choices
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


class House(models.Model):
    address = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    living_rooms = models.IntegerField(default=0)

    def __str__(self):
        return self.address


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

    comment_length = 280

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


    # Basic Info
    house_filed = models.ForeignKey('reviews.House', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    moved_in_date = models.DateField(blank=True, null=True)
    moved_out_date = models.DateField(blank=True, null=True)

    # Landlord
    landlord_responsiveness = RatingField(mandatory=True)
    landlord_responsiveness_comment = models.CharField(max_length=comment_length, blank=True, null=True)

    repair_quality = RatingField()
    repair_quality_comment = models.CharField(max_length=comment_length, blank=True, null=True)

    # Construction Quality
    water_pressure = RatingField(mandatory=True)
    water_pressure_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    utilities = RatingField(mandatory=True)
    utilities_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    furniture_quality = RatingField()
    furniture_quality_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    mattress_quality = RatingField()
    mattress_quality_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    build_quality = RatingField()
    build_quality_comment = models.CharField(max_length=comment_length, blank=True, null=True)

    # Nuisances
    quietness = RatingField(mandatory=True)
    quietness_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    pest_free = RatingField(mandatory=True)
    pest_free_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    smells = RatingField()
    smells_comment = models.CharField(max_length=comment_length, blank=True, null=True)
    damp_mould_free = RatingField()
    damp_mould_free_comment = models.CharField(max_length=comment_length, blank=True, null=True)

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
            rating += self.landlord_responsiveness * HouseReport.landlord_responsiveness_weight
            total_report_weight += HouseReport.landlord_responsiveness_weight
        if hasattr(self, 'repare_quality'):
            rating += self.repare_quality * HouseReport.repair_quality_weight
            total_report_weight += HouseReport.repair_quality_weight
        if hasattr(self, 'water_pressure'):
            rating += self.water_pressure * HouseReport.water_pressure_weight
            total_report_weight += HouseReport.water_pressure_weight
        if hasattr(self, 'utilities'):
            rating += self.utilities * HouseReport.utilities_weight
            total_report_weight += HouseReport.utilities_weight
        if hasattr(self, 'furniture_quality'):
            rating += self.furniture_quality * HouseReport.furniture_quality_weight
            total_report_weight += HouseReport.furniture_quality_weight
        if hasattr(self, 'mattress_quality'):
            rating += self.mattress_quality * HouseReport.mattress_quality_weight
            total_report_weight += HouseReport.mattress_quality_weight
        if hasattr(self, 'build_quality'):
            rating += self.build_quality * HouseReport.build_quality_weight
            total_report_weight += HouseReport.build_quality_weight
        if hasattr(self, 'quietness'):
            rating += self.quietness * HouseReport.quietness_weight
            total_report_weight += HouseReport.quietness_weight
        if hasattr(self, 'pest_free'):
            rating += self.pest_free * HouseReport.pest_free_weight
            total_report_weight += HouseReport.pest_free_weight
        if hasattr(self, 'smells'):
            rating += self.smells * HouseReport.smells_weight
            total_report_weight += HouseReport.smells_weight
        if hasattr(self, 'damp_mould_free'):
            rating += self.damp_mould_free * HouseReport.damp_mould_free_weight
            total_report_weight += HouseReport.damp_mould_free_weight
        rating = rating / total_report_weight
        self.general_rating = round(rating*10)/10
        return rating
