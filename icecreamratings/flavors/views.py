import json

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (DetailView, TemplateView,
                                  CreateView, UpdateView,
                                  ListView, View)
from django.http import HttpResponse
from django.utils.functional import cached_property
from django.contrib import messages
from django.core import serializers
from django.views.generic import ListView

from braces.views import LoginRequiredMixin

from core.utils import check_sprinkle_rights
from core.views import TitleSearchMixin
from core.models import ModelFormFailureHistory
from .decorators import check_sprinkles
from .models import Sprinkle, Flavor, Taster
from .forms import FlavorForm, TasterForm
from .tasks import update_users_who_favorited
from .reports import make_flavor_pdf


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
                  'sprinkles/sprinkle_preview.html',
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

    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(FlavorActionMixin, self).form_valid(form)

    def form_invalid(self, form):
        """
        Сохраним невалидную форму и модель для изучения.
        """
        form_data = json.dumps(form.cleaned_data)
        model_data = serializers.serialize('json',
                                           [form.instance])[1:-1]
        ModelFormFailureHistory.objects.create(
            form_data=form_data,
            model_data=model_data
        )
        return super(FlavorActionMixin, self).form_invalid(form)


class FavoriteUpdateView(LoginRequiredMixin, FavoriteMixin,
                         FlavorActionMixin, UpdateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
    success_msg = 'Flavor updated!'
    form_class = FlavorForm

    def form_valid(self, form):
        update_users_who_favorited(
            instance=self.object,
            favorites=self.likes_and_favorites['favorites']
        )
        return super(FlavorCreateView, self).form_valid(form)


class FlavorDetailView(LoginRequiredMixin, FavoriteMixin, DetailView):
    model = Flavor


class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin,
                       CreateView):
    model = Flavor
    fields = ('title', 'slug', 'scoops_remaining')
    success_msg = 'Flavor created!'
    form_class = FlavorForm

    def form_valid(self, form):
        # Здесь может быть кастомная логика
        return super(FlavorCreateView, self).form_valid(form)

    def form_invalid(self, form):
        # Здесь кастомная логика для для действий с невалидной формой
        return super(FlavorCreateView, self).form_invalid(form)


class FlavorListView(TitleSearchMixin, ListView):
    model = Flavor


class FlavorView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Управляем отображением объекта Flavor
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
        return render(request,
                      'flavors/flavor_detail.html',
                      {'flavor': flavor}
                      )

    def post(self, request, *args, **kwargs):
        # Упраляем обновлением объекта Flavor
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])
        form = FlavorForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('flavors:detail', flavor.slug)


class PDFFlavorView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Получаем flavor
        flavor = get_object_or_404(Flavor, slug=kwargs['slug'])

        # создаем response
        response = HttpResponse(content_type='application/pdf')

        # генерируем pdf и прикладываем к response
        response = make_flavor_pdf(response, flavor)

        return response


class TasterUpdateView(LoginRequiredMixin, UpdateView):
    model = Taster
    form_class = TasterForm
    success_url = '/someplace/'

    def get_form_kwargs(self):
        """
        Этот метод делает инъекцию в форму по ключевым аргументам
        """
        # захватим текущий набор кваргов формы
        kwargs = super(TasterUpdateView, self).get_form_kwargs()
        # обновим кварги с user_id
        kwargs['user'] = self.request.user
        return kwargs