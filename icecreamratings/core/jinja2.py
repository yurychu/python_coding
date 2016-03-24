import random

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.template import defaultfilters

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'dj': defaultfilters,
        # {{ random }}
        'random_once': random.randint(1, 5),
        # {{ random() }}
        'random': lambda: random.randint(1, 5),
    })
    return env
