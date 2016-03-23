from django.db import models
from django.core.urlresolvers import reverse
from .managers import VoucherManager


class Voucher(models.Model):
    """
    Ваучеры для 3 пинт бесплатного мороженого
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    birth_date = models.DateField(blank=True)
    sent = models.BooleanField(default=False)
    radeemed = models.BooleanField(default=False)

    objects = VoucherManager()
