# -*- coding: utf-8 -*-
from django.http import HttpResponse
import datetime


def hello(request):
    return HttpResponse("Привет чувак")


def home(request):
    return HttpResponse("Хоме пейдж")


def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html><body>Сейчас %s</body></html>' % now
    return HttpResponse(html)

