from functools import wraps

from core import utils


def check_sprinkles(view_func):
    """
    Проверяет, что юзер может добавлять sprinkles
    """
    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        # Действие с request объектом с utils.can_spikle_rights()
        request = utils.check_sprinkle_rights(request)

        # Вызов функции представления
        response = view_func(request, *args, **kwargs)

        return response
    return new_view_func
