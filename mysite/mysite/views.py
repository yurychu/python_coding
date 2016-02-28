# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from forms import ContactForm
from django.template import RequestContext

from books.models import Book


def hello(request):
    return HttpResponse("Привет чувак")


def home(request, ho_lo):
    return HttpResponse("Хоме пейдж" + ho_lo)


def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('hours_ahead.html', {'offset': offset, 'dt': dt})


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term')
        elif len(q) > 20:
            errors.append('Please enter at most 20 char')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_results.html',
                                      {'books': books, 'query': q})
    return render_to_response('search_form.html', {'errors': errors})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks')
    else:
        form = ContactForm(
            initial={'subject': 'I love your site!'}
        )
    return render_to_response('contact_form.html', {'form': form})


def contact_thanks(request):
    return HttpResponse('Thanks')


def object_list(request, model):
    obj_list = model.objects.all()
    obj_name = model.__name__.lower() + '_list'
    template_name = '%s.html' % obj_name
    return render_to_response(template_name, {obj_name: obj_list})
