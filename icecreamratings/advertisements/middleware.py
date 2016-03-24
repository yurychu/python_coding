import random

from advertisements.models import Advertisement as Ad


def AdvertisementMiddleware(object):

    def process_request(request):
        count = Ad.objects.filter(subject='ice-cream').count()
        ads = Ad.objects.filter(subject='ice-cream')

        # Если необходимо добавим переменную контекста в request object
        if not hasattr(request, 'context'):
            request.context = {}

        # Не перезаписываем контекст, вместо этого билдим его:
        request.context.update({'ad': ads[random.randrange(0, count)]})
