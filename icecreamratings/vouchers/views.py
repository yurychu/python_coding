from django.views.generic import TemplateView

from .models import Voucher


class GreenfeldRoyView(TemplateView):
    template_name = 'vouchers/views_conditional.html'

    def get_context_data(self, **kwargs):
        context = super(GreenfeldRoyView,
                        self).get_context_data(**kwargs)
        context['greenfelds'] = Voucher.objects.filter(
            name__icontains='greenfeld')
        context['roys'] = Voucher.objects.filter(
            name__icontains='roy')
        return context

