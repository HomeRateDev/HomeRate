from django.db.models.functions import datetime
from django.test import TestCase
from pytz import UTC

from .models import House


class ReviewsTest(TestCase):
    def setUp(self):
        return 0

    def testMakeAndRecallHouseModel(self):
        time1 = datetime.datetime(year=2018, month=5, day=30, tzinfo=UTC)
        time2 = datetime.datetime(year=2018, month=2, day=15, tzinfo=UTC)
        House.objects.create(address="10 Downing Street", date_created=time1)
        House.objects.create(address="101 Dalmatian lane", date_created=time2)
        house1 = House.objects.get(address="10 Downing Street")
        house2 = House.objects.get(address="101 Dalmatian lane")
        self.assertEqual(house1.date_created, time1)
        self.assertEqual(house2.date_created, time2)
