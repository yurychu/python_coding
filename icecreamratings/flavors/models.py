from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from core.models import TimeStampedModel


STATUS = (
    (0, 'zero'),
    (1, 'one'),
)


class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    scoops_remaining = models.IntegerField(default=0, choices=STATUS)

    def get_absolute_url(self):
        return reverse('flavors:detail', kwargs={'slug': self.slug})


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
