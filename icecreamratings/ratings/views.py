from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from flavors.models import Flavor
from promos.models import Promo

from store.exceptions import OutOfStock, CorruptedDatabase


def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = "Multiple items have SKU {}. Please fix!".format(sku)
        raise CorruptedDatabase


def list_any_line_item(model, sku):
    try:
        return model.objects.get(sku=sku, quantity__gt=0)
    except ObjectDoesNotExist:
        msg = "We are out of {0}.format(sku)"
        raise OutOfStock(msg)


def fun_function(**kwargs):
    """
    Ищет рабочее промо мороженого
    """
    results = Promo.objects.active()
    results = results.filter(
        Q(name__startswith=name) |
        Q(description__icontains=name)
    )
    results = results.exclude(status='melted')
    results = results.select_releated('flavors')
    return results
