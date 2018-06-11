# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from core.ratings import RatingField


def round2sf(num):
    return round(num*10)/10


# Create your models here.


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
        return round2sf(total_report_rating)





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

    # Image
    image = models.ImageField(upload_to='media/%Y/%m/%d/%s', default='default.png', blank=True, null=True)

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
        if hasattr(self, 'landlord_responsiveness') and self.landlord_responsiveness is not '':
            rating += int(self.landlord_responsiveness) * HouseReport.landlord_responsiveness_weight
            total_report_weight += HouseReport.landlord_responsiveness_weight
        if hasattr(self, 'repair_quality') and self.repair_quality is not '':
            rating += int(self.repair_quality) * HouseReport.repair_quality_weight
            total_report_weight += HouseReport.repair_quality_weight
        if hasattr(self, 'water_pressure') and self.water_pressure is not '':
            rating += int(self.water_pressure) * HouseReport.water_pressure_weight
            total_report_weight += HouseReport.water_pressure_weight
        if hasattr(self, 'utilities') and self.utilities is not '':
            rating += int(self.utilities) * HouseReport.utilities_weight
            total_report_weight += HouseReport.utilities_weight
        if hasattr(self, 'furniture_quality') and self.furniture_quality is not '':
            rating += int(self.furniture_quality) * HouseReport.furniture_quality_weight
            total_report_weight += HouseReport.furniture_quality_weight
        if hasattr(self, 'mattress_quality') and self.mattress_quality is not '':
            rating += int(self.mattress_quality) * HouseReport.mattress_quality_weight
            total_report_weight += HouseReport.mattress_quality_weight
        if hasattr(self, 'build_quality') and self.build_quality is not '':
            rating += int(self.build_quality) * HouseReport.build_quality_weight
            total_report_weight += HouseReport.build_quality_weight
        if hasattr(self, 'quietness') and self.quietness is not '':
            rating += int(self.quietness) * HouseReport.quietness_weight
            total_report_weight += HouseReport.quietness_weight
        if hasattr(self, 'pest_free') and self.pest_free is not '':
            rating += int(self.pest_free) * HouseReport.pest_free_weight
            total_report_weight += HouseReport.pest_free_weight
        if hasattr(self, 'smells') and self.smells is not '':
            rating += int(self.smells) * HouseReport.smells_weight
            total_report_weight += HouseReport.smells_weight
        if hasattr(self, 'damp_mould_free') and self.damp_mould_free is not '':
            rating += int(self.damp_mould_free) * HouseReport.damp_mould_free_weight
            total_report_weight += HouseReport.damp_mould_free_weight
        rating = rating / total_report_weight
        self.general_rating = round2sf(rating)
        return rating
