# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class House(models.Model):
    address = models.CharField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.addr


class HouseReport(models.Model):
    house_filed = models.ForeignKey('reviews.House', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    moved_in_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    pros = models.TextField()
    cons = models.TextField()
    monthly_cost = models.DecimalField(max_digits=6, decimal_places=2)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.house_filed) + " - " + str(self.author) + " - " + str(self.moved_in_date)