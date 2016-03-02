"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, ListView

from mysite import views
from books import models

publisher_info = {
    'queryset': models.Publisher.objects.all(),
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<home1>\d)/(?P<home2>\d)/$', views.home),
    url(r'^authors/$', views.object_list, {'model': models.Author}),
    url(r'^my-image/$', views.my_image),
    url(r'^hello-pdf/$', views.hello_pdf),
    url(r'^show_color/$', views.show_color),
    url(r'^set_color/$', views.set_color),
    # url(r'^books/', include('books.urls')),
    # url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    # url(r'^publisher/$', ListView.as_view(), publisher_info),
    # url(r'^hello/$', views.hello),
    # url(r'^time/$', views.current_datetime),
    # url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
    # url(r'^show_meta', display_meta),
    # url(r'^search/$', search),
    # url(r'^contact/$', contact),
    # url(r'^contact/thanks$', contact_thanks)
]
