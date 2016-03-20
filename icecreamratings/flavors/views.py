from django.shortcuts import render, get_object_or_404
from django.views.generic import (DetailView, TemplateView,
                                  CreateView, UpdateView,
                                  ListView)
from django.utils.functional import cached_property
from django.contrib import messages

from braces.views import LoginRequiredMixin

from core.utils import check_sprinkle_rights
from .decorators import check_sprinkles
from .models import Sprinkle, Flavor
from .tasks import update_users_who_favorited


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


class FreshFruitMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FreshFruitMixin, self).get_context_data(**kwargs)
        context['has_fresh_fruit'] = True
        return context


class FruityFlavorView(FreshFruitMixin, TemplateView):
    template_name = 'fruity_flavor.html'


class FavoriteMixin(object):

    @cached_property
    def likes_and_favorites(self):
        """
        Возвращает словарь предпочтений
        """
        likes = self.object.likes()
        favorites = self.object.favorites()
        return {
            'likes': likes,
            'favorites': favorites,
            'favorites_count': favorites.count()
        }


class FlavorActionMixin(object):
    fields = ('title', 'slug', 'scoops_remaining')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)


class FavoriteUpdateView(LoginRequiredMixin, FavoriteMixin,
                         FlavorActionMixin, UpdateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
    success_msg = 'Flavor updated!'

    def form_valid(self, form):
        update_users_who_favorited(
            instance=self.object,
            favorites=self.likes_and_favorites['favorites']
        )
        return super(FlavorCreateView, self).form_valid(form)


class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, DetailView):
    model = Flavor


class FlavorCreateView(LoginRequiredMixin, CreateView,
                       FlavorActionMixin):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
    success_msg = 'Flavor created!'

    def form_valid(self, form):
        # Здесь может быть кастомная логика
        return super(FlavorCreateView, self).form_valid(form)

    def form_invalid(self, form):
        # Здесь кастомная логика для для действий с невалидной формой
        return super(FlavorCreateView, self).form_invalid(form)


class FlavorListView(ListView):
    model = Flavor

    def get_queryset(self):
        # достанем кверисет из родительского кверисета
        queryset = super(FlavorListView, self).get_queryset()

        # получим q параметр
        q = self.request.GET.get('q')
        if q:
            # Возвращаем отфильтрованный кверисет
            return queryset.filter(title__icontains=q)
        # возвращаемся на базовый кверисет
        return queryset
