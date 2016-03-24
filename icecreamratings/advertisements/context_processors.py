import random

from advertisements.models import Advertisement


def advertisements(request):
    count = Advertisement.objects.filter(subject='ice-cream').count()
    ads = Advertisement.objects.filter(subject='ice-cream')
    return {'ad': ads[random.randrange(0, count)]}
