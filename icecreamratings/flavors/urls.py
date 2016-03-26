from django.conf.urls import url

from flavors import views


urlpatterns = [
    url(
        regex=r'^api/$',
        view=views.FlavorCreateReadView.as_view(),
        name='flavor_rest_api'
        ),
    url(
        regex=r'^api/(?P<slug>[-\w]+)$',
        view=views.FlavorReadUpdateDeleteView.as_view(),
        name='flavor_rest_api'
    ),
]
