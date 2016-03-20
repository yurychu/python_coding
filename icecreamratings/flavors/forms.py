import csv
from io import StringIO

from django import forms

from .models import Seller, Purchase, Taster


class FlavorForm:
    pass


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase

    def clean_seller(self):
        seller = self.cleaned_data['seller']
        try:
            Seller.objects.get(name=seller)
        except Seller.DoesNotExist:
            msg = '{0} does not exist in purchase #{1}.'.format(
                seller,
                self.cleaned_data['purchase_num']
            )
            raise forms.ValidationError(msg)
        return seller


def add_csv_purchases(rows):

    rows = StringIO(rows)

    records_added = 0
    errors = []

    # генерируем словарь на строку, первая csv строка будет ключами
    for row in csv.DictReader(rows, delimiter=','):
        # биндим данные в PurchaseForm
        form = PurchaseForm(row)
        if form.is_valid():
            # Валидные строчные данные записываем
            form.save()
            records_added += 1
        else:
            errors.append(form.errors)

    return records_added, errors


class TasterForm(forms.ModelForm):

    class Meta:
        model = Taster

    def __init__(self):
        # устанавливаем пользователя как атрибут формы
        self.user = kwargs.pop('user')
        super(TasterForm, self).__init__(*args, **kwargs)
