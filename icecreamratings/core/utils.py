from django.core.exceptions import PermissionDenied
import functools


def check_sprinkle_rights(request):
    if request.user.can_sprinkle or request.user.is_staff:
        # если еще добавим это значение после проверки,
        # то оно облегчит логику в наших шаблонах
        # например, вместо этого
        # {% if request.user.can_sprinkle or request.user.is_staff %}
        # можно просто выполнить
        # {% if request.can_sprinkle %}
        request.can_sprinkle = True
        return request

    # иначе возвращаем исключение 403
    return PermissionDenied


# Простой шаблон декоратора
def decorator(view_func):
    @functools.wraps(view_func)
    def new_veiw_func(request, *args, **kwargs):
        # Тут мы можем модифицировать request (HttpRequest)
        response = view_func(request, *args, **kwargs)
        # Так же можно модифицировать response (HttpResponse)
        return response
    return new_veiw_func
