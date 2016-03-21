from django.db import models


class TimeStampedModel(models.Model):
    """
    Абстрактный базовый класс, который предоставляет самообновляющиеся поля
    created и modified
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelFormFailureHistory(models.Model):
    form_data = models.TextField()
    model_data = models.TextField()