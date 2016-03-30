"""
Вызывается из root urls.py например
url(r'^api/', include('core.api', namespace='api')),
"""
from django.conf.urls import url

from flavors import views as flavor_views
from users import views as user_views


urlpatterns = [
    # {% url 'api:flavors %}
    url(
        regex=r'^flavors/$',
        view=flavor_views.FlavorCreateReadView.as_view(),
        name='flavors'
    ),
    # {% url 'api:flavors' flavor.slug %}
    url(
        regex=r'^flavors/(?P<slug>[-\w]+/$',
        view=flavor_views.FlavorReadUpdateDeleteView.as_view(),
        name='flavors'
    ),
    # {% url 'api:users' %}
    url(
        regex=r'^users/$',
        view=user_views.UserCreateReadView.as_view(),
        name='users'
    ),
    # {% url 'api:users' user.slug %}
    url(
        regex=r'^users/(?P<slug>[-\w]+/$',
        view=user_views.UserReadUbdateDeleteView.as_view(),
        name='users'
    ),
]
