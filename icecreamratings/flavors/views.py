from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from core.utils import check_sprinkle_rights
from .decorators import check_sprinkles
from .models import Sprinkle


def sprinkle_list(request):
    """
    Стандартное представление списка
    """
    request = check_sprinkle_rights(request)

    return render(request,
                  'sprinkles/sprinkle_list.html',
                  {'sprinkles': Sprinkle.objects.all()})


@check_sprinkles
def sprinkle_detail(request):
    """
    Стандартное представление элементов модели
    """

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


class SprinkleDetail(DetailView):
    """
    Стандартный представление подробностей
    """
    model = Sprinkle

    def dispatch(self, request, *args, **kwargs):
        request = check_sprinkle_rights(request)
        return super(SprinkleDetail, self).dispatch(
            request, *args, **kwargs
        )
