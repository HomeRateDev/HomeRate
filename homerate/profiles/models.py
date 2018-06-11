from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from core.ratings import RatingField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    # Landlord
    landlord_responsiveness = RatingField(mandatory=True, weighting=True, default=2)

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

    # other fields...

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
