from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from .models import Flavor


class FlavorBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

    def show_url(self, instance):
        url = reverse('flavor_bar_detail',
                      kwargs={'pk': instance.pk})
        response = format_html('''<a href="{0}">{1}</a>''', url, url)
        return response

    show_url.short_description = "Flavor Bar URL"
    show_url.allow_tags = True


admin.site.register(Flavor, FlavorBarAdmin)
