from django.shortcuts import render, get_object_or_404

from core.utils import check_sprinkle_rights
from .models import Sprinkle


def sprinkle_list(request):
    """
    Стандартное представление списка
    """
    request = check_sprinkle_rights(request)

    return render(request,
                  'sprinkles/sprinkle_list.html',
                  {'sprinkles': Sprinkle.objects.all()})


def sprinkle_detail(request):
    """
    Стандартное представление элементов модели
    """
    request = check_sprinkle_rights(request)

    sprinkle = get_object_or_404(Sprinkle, pk=pk)

    return render(request,
                  'sprinkles/sprinkle_detail.html',
                  {'sprinkle': sprinkle})


def sprinkle_preview(request):
    """
    Предпросмотр нового sprinkle, но без check_sprinkles
    """
    sprinkle = Sprinkle.objects.all()
    return render(request,
                  'sprinkle/sprinkle_preview.html',
                  {'sprinkle': sprinkle})
