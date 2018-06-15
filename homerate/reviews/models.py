# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from core.ratings import RatingField


def round2sf(num):
    return round(num*10)/10


# Create your models here.


class House(models.Model):
    address = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    living_rooms = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.address

    def split_address(self):
        components = self.address.split(",")
        return {
            'line1': components[0],
            'line2': components[-2] + ", " + components[-3],
            'postcode': components[-1][:-3] + " " + components[-1][-3:]
        }

    def get_address(self):
        return self.address[:-3] + " " + self.address[-3:]

    def general_star_rating(self):
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

    def personal_star_rating(self, user_profile):
        reports = HouseReport.objects.filter(house_filed=self).order_by('-moved_out_date')
        time_dependant_rating_weight = 1
        time_dependant_rating_weight_total = 0
        total_report_rating = 0
        if len(reports) == 0:
            return None
        for report in reports:
            total_report_rating += report.get_personal_rating(user_profile) * time_dependant_rating_weight
            time_dependant_rating_weight_total += time_dependant_rating_weight
            time_dependant_rating_weight = time_dependant_rating_weight * 0.6

        total_report_rating = total_report_rating / time_dependant_rating_weight_total
        self.average_rating = total_report_rating
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

    # Basic Info
    house_filed = models.ForeignKey('reviews.House', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    moved_in_date = models.DateField(blank=True, null=True)
    moved_out_date = models.DateField(blank=True, null=True)
    reported_by = models.ManyToManyField('auth.User', blank=True, related_name='users_who_reported')
    visible = models.BooleanField(default=True)

    # Landlord
    landlord_responsiveness = RatingField(mandatory=True)
    repair_quality = RatingField()
    landlord_comment = models.CharField(max_length=comment_length, blank=True, null=True)

    # Construction Quality
    water_pressure = RatingField(mandatory=True)
    utilities = RatingField(mandatory=True)
    furniture_quality = RatingField()
    mattress_quality = RatingField()
    build_quality = RatingField()
    construction_quality_comment = models.CharField(max_length=comment_length, blank=True, null=True)

    # Nuisances
    quietness = RatingField(mandatory=True)
    pest_free = RatingField(mandatory=True)
    smells = RatingField()
    damp_mould_free = RatingField()
    nuisances_comment = models.CharField(max_length=comment_length, blank=True, null=True)

    # Affordability
    monthly_rent = models.IntegerField(default=0)
    monthly_bills = models.IntegerField(default=0)
    affordability_comment = models.CharField(max_length=comment_length, blank=True, null=True)

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


    def get_personal_rating(self, user_profile):
        total_report_weight = 0
        rating = 0
        if hasattr(self, 'landlord_responsiveness') and self.landlord_responsiveness is not '':
            rating += int(self.landlord_responsiveness) * int(user_profile.landlord_responsiveness)
            total_report_weight += int(user_profile.landlord_responsiveness)
        if hasattr(self, 'repair_quality') and self.repair_quality is not '':
            rating += int(self.repair_quality) * int(user_profile.repair_quality)
            total_report_weight += int(user_profile.repair_quality)
        if hasattr(self, 'water_pressure') and self.water_pressure is not '':
            rating += int(self.water_pressure) * int(user_profile.water_pressure)
            total_report_weight += int(user_profile.water_pressure)
        if hasattr(self, 'utilities') and self.utilities is not '':
            rating += int(self.utilities) * int(user_profile.utilities)
            total_report_weight += int(user_profile.utilities)
        if hasattr(self, 'furniture_quality') and self.furniture_quality is not '':
            rating += int(self.furniture_quality) * int(user_profile.furniture_quality)
            total_report_weight += int(user_profile.furniture_quality)
        if hasattr(self, 'mattress_quality') and self.mattress_quality is not '':
            rating += int(self.mattress_quality) * int(user_profile.mattress_quality)
            total_report_weight += int(user_profile.mattress_quality)
        if hasattr(self, 'build_quality') and self.build_quality is not '':
            rating += int(self.build_quality) * int(user_profile.build_quality)
            total_report_weight += int(user_profile.build_quality)
        if hasattr(self, 'quietness') and self.quietness is not '':
            rating += int(self.quietness) * int(user_profile.quietness)
            total_report_weight += int(user_profile.quietness)
        if hasattr(self, 'pest_free') and self.pest_free is not '':
            rating += int(self.pest_free) * int(user_profile.pest_free)
            total_report_weight += int(user_profile.pest_free)
        if hasattr(self, 'smells') and self.smells is not '':
            rating += int(self.smells) * int(user_profile.smells)
            total_report_weight += int(user_profile.smells)
        if hasattr(self, 'damp_mould_free') and self.damp_mould_free is not '':
            rating += int(self.damp_mould_free) * int(user_profile.damp_mould_free)
            total_report_weight += int(user_profile.damp_mould_free)
        rating = rating / total_report_weight
        self.general_rating = round2sf(rating)
        return rating

    @staticmethod
    def make_aggregate(reports):
        aggregate = {'landlord_responsiveness': 0, 'repair_quality': 0, 'water_pressure': 0,
                     'utilities': 0, 'furniture_quality': 0, 'mattress_quality': 0,
                     'build_quality': 0, 'quietness': 0, 'pest_free': 0,
                     'smells': 0, 'damp_mould_free': 0, 'landlord_overall': 0}
        aggregate_t = {'landlord_responsiveness': 0, 'repair_quality': 0, 'water_pressure': 0,
                     'utilities': 0, 'furniture_quality': 0, 'mattress_quality': 0,
                     'build_quality': 0, 'quietness': 0, 'pest_free': 0,
                     'smells': 0, 'damp_mould_free': 0}

        time_weighting = 1
        time_factor = 0.8
        for report in reports:
            if hasattr(report, 'landlord_responsiveness') and report.landlord_responsiveness is not '':
                aggregate['landlord_responsiveness'] += int(report.landlord_responsiveness) * time_weighting
                aggregate_t['landlord_responsiveness'] += time_weighting
            if hasattr(report, 'repair_quality') and report.repair_quality is not '':
                aggregate['repair_quality'] += int(report.repair_quality) * time_weighting
                aggregate_t['repair_quality'] += time_weighting
            if hasattr(report, 'water_pressure') and report.water_pressure is not '':
                aggregate['water_pressure'] += int(report.water_pressure) * time_weighting
                aggregate_t['water_pressure'] += time_weighting
            if hasattr(report, 'utilities') and report.utilities is not '':
                aggregate['utilities'] += int(report.utilities) * time_weighting
                aggregate_t['utilities'] += time_weighting
            if hasattr(report, 'furniture_quality') and report.furniture_quality is not '':
                aggregate['furniture_quality'] += int(report.furniture_quality) * time_weighting
                aggregate_t['furniture_quality'] += time_weighting
            if hasattr(report, 'mattress_quality') and report.mattress_quality is not '':
                aggregate['mattress_quality'] += int(report.mattress_quality) * time_weighting
                aggregate_t['mattress_quality'] += time_weighting
            if hasattr(report, 'build_quality') and report.build_quality is not '':
                aggregate['build_quality'] += int(report.build_quality) * time_weighting
                aggregate_t['build_quality'] += time_weighting
            if hasattr(report, 'quietness') and report.quietness is not '':
                aggregate['quietness'] += int(report.quietness) * time_weighting
                aggregate_t['quietness'] += time_weighting
            if hasattr(report, 'pest_free') and report.pest_free is not '':
                aggregate['pest_free'] += int(report.pest_free) * time_weighting
                aggregate_t['pest_free'] += time_weighting
            if hasattr(report, 'smells') and report.smells is not '':
                aggregate['smells'] += int(report.smells) * time_weighting
                aggregate_t['smells'] += time_weighting
            if hasattr(report, 'damp_mould_free') and report.damp_mould_free is not '':
                aggregate['damp_mould_free'] += int(report.damp_mould_free) * time_weighting
                aggregate_t['damp_mould_free'] += time_weighting
            time_weighting *= time_factor

        for key in aggregate_t:
            if aggregate_t[key] != 0:
                aggregate[key] /= aggregate_t[key]


        if aggregate_t['landlord_responsiveness'] != 0:
            aggregate['landlord_overall'] += aggregate['landlord_responsiveness']
        if aggregate_t['repair_quality'] != 0:
            aggregate['landlord_overall'] += aggregate['repair_quality']
        if aggregate_t['landlord_responsiveness'] != 0 and aggregate_t['repair_quality'] != 0:
            aggregate['landlord_overall'] /= 2


        return aggregate


class ReviewImage(models.Model):
    # Linked house report
    house_report = models.ForeignKey('reviews.HouseReport', on_delete=models.CASCADE)
    # Image
    image = models.ImageField(upload_to='media/%Y/%m/%d/%s', blank=True, null=True)
