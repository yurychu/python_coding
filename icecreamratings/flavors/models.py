from django.db import models

from core.models import TimeStampedModel


class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)
