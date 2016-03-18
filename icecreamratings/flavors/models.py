from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel


class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)


class PublishedManager(models.Manager):

    use_for_related_fields = True

    def published(self, **kwargs):
        return self.filter(pub_date__lte=timezone.now(), **kwargs)


class FlavorReview(models.Model):
    review = models.CharField(max_length=255)
    pub_date = models.DateTimeField()

    # добавляем кастомную модель менеджера (переименовываем objects)
    objects = PublishedManager()


class Sprinkle(models.ModelK):
    pass
