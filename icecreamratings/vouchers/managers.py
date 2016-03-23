from django.utils import timezone

from dateutil.relativedelta import relativedelta

from django.db import models


class VoucherManager(models.Manager):

    def age_breakdown(self):
        """
        Возвращает список словарей с соритрованными данными
        """
        age_brackets = []
        now = timezone.now()

        delta = now - relativedelta(year=18)
        count = self.model.objects.filter(birth_date__gt=delta).count()
        age_brackets.append(
            {'title': '0-17', 'count': count}
        )
        count = self.model.objects.filter(birth_date__lte=delta).count()
        age_brackets.append(
            {'title': '18+', 'count': count}
        )
        return age_brackets
