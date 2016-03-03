# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm

from forms import ContactForm
from django.template import RequestContext

from books.models import Book

from reportlab.pdfgen import canvas


def hello(request):
    return HttpResponse("Привет чувак")


def home(request, home1, home2):
    return HttpResponse("Хоме пейдж" + str(home2) + str(home1))


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


def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request, *args, **kwargs)
    return new_view


def my_image(request):
    image_data = open('tmp/копии-учредит-документов.jpg')
    return HttpResponse(image_data, content_type='image/png')


def hello_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    p = canvas.Canvas(response)

    p.drawString(100, 100, 'Hello world')

    p.showPage()
    p.save()
    return response


@login_required
def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Your favorite color is %s" %
                            request.COOKIES["favorite_color"])
    else:
        return HttpResponse("You dont save a color")


def set_color(request):
    if "favorite_color" in request.GET:
        response = HttpResponse("Your favorite color is now %s" %
                                request.GET["favorite_color"])
        response.set_cookie('favorite_color',
                            request.GET["favorite_color"])
        return response
    else:
        return HttpResponse("Your didnt give a favorite color")


def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/account/logged-in')
    else:
        return HttpResponseRedirect('/account/login-error')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/account/logout')


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.save(data)
            return HttpResponseRedirect('/show_color/')
    else:
        data, errors = {}, {}
    return render_to_response('my_register.html', {'form': form, 'errors': errors})