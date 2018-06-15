from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from core.ratings import RatingField
from reviews.models import House, HouseReport


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    is_suspicious = models.BooleanField(default=False)

    saved_houses = models.ManyToManyField(House, blank=True)

    # Landlord
    landlord_responsiveness = RatingField(mandatory=True, weighting=True, default=2)

    # Repairs
    repair_quality = RatingField(mandatory=True, weighting=True, default=2)

    # Construction Quality
    water_pressure = RatingField(mandatory=True, weighting=True, default=2)
    utilities = RatingField(mandatory=True, weighting=True, default=2)
    furniture_quality = RatingField(mandatory=True, weighting=True, default=2)
    mattress_quality = RatingField(mandatory=True, weighting=True, default=2)
    build_quality = RatingField(mandatory=True, weighting=True, default=2)

    # Nuisances
    quietness = RatingField(mandatory=True, weighting=True, default=2)
    pest_free = RatingField(mandatory=True, weighting=True, default=2)
    smells = RatingField(mandatory=True, weighting=True, default=2)
    damp_mould_free = RatingField(mandatory=True, weighting=True, default=2)

    # Postcode
    postcode_max_length = 8
    postcode = models.CharField(max_length=postcode_max_length, blank=True, null=True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.user.first_name

    def getPostcode(self):
        if not self.postcode is None:
            p = self.postcode.replace(" ", "")
            return p[:-3] + " " + p[-3:]
        else:
            return None