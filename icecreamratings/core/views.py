

class TitleSearchMixin(object):

    def get_queryset(self):
        # извлечем queryset из родительского get_queryset
        queryset = super(TitleSearchMixin, self).get_queryset()

        # получим q GET параметр
        q = self.request.GET.get('q')
        if q:
            # возвращаем отфильтрованный queryset
            return queryset.filter(title__icontains=q)
        # в отсутствии q вернем queryset
        return queryset
