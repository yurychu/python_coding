from django.core.exceptions import ValidationError


def validate_tasty(value):
    """
    Генерирует исключение валидации,
    если ввденое значение не начинается с 'Tasty'
    """
    if not value.startswith('Tasty'):
        msg = 'Необходимо начинать с Tasty'
        raise ValidationError(msg)
