from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from core.models import TimeStampedModel, TastyTitleAbstractModel


STATUS = (
    (0, 'zero'),
    (1, 'one'),
)


@python_2_unicode_compatible
class Flavor(TastyTitleAbstractModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    scoops_remaining = models.IntegerField(default=0, choices=STATUS)

    def __str__(self):
        return self.title

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


class Sprinkle(models.Model):
    pass


class Purchase(models.Model):
    pass


class Seller(models.Model):
    pass


class Taster(models.Model):
    pass
