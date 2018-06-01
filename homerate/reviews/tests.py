from django.contrib.auth.models import User
from django.db.models.functions import datetime
from django.test import TestCase
from pytz import UTC

from .models import House, HouseReport


class ReviewsTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('Testy', 'testy@tests.com', 'password1234')
        return 0

    def tearDown(self):
        # Clean up after each test
        self.user_1.delete()

    def testMakeAndRecallHouseModel(self):
        time1 = datetime.datetime(year=2018, month=5, day=30, tzinfo=UTC)
        time2 = datetime.datetime(year=2018, month=2, day=15, tzinfo=UTC)
        House.objects.create(address="10 Downing Street", date_created=time1)
        House.objects.create(address="101 Dalmatian Lane", date_created=time2)
        house1 = House.objects.get(address="10 Downing Street")
        house2 = House.objects.get(address="101 Dalmatian Lane")
        self.assertEqual(house1.date_created, time1)
        self.assertEqual(house2.date_created, time2)


    def testMakeAndRecallHouseReport(self):
        house = House(address="13 NeverLand Lane", date_created=datetime.datetime(2018, 4, 3, tzinfo=UTC))
        house.save()
        houseReport = HouseReport(house_filed=house, author=self.user_1,
                                  moved_in_date=datetime.datetime(2018, 1, 3, tzinfo=UTC),
                                  description="description",
                                  pros="pros",
                                  cons="cons",
                                  monthly_cost=1000)
        houseReport.save()
        reports = HouseReport.objects.filter(house_filed=house)
        self.assertEqual(len(reports), 1)
        self.assertEquals(reports[0], houseReport)
