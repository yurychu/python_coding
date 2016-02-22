# -*- coding: utf-8 -*-
import datetime

from django.http import HttpResponse, Http404
from django.template import Template, Context


def hello(request):
    return HttpResponse("Привет чувак")


def home(request):
    return HttpResponse("Хоме пейдж")


def current_datetime(request):
    now = datetime.datetime.now()
    t = Template('<html><body>Сейчас {{ current_date }}</body></html>')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
