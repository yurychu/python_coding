from django.core.exceptions import PermissionDenied


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
