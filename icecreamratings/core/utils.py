from django.core.exceptions import PermissionDenied


def check_sprinkle_rights(request):
    if request.user.can_sprinkle or request.user.is_staff:
        return request

    # иначе возвращаем исключение 403
    return PermissionDenied
