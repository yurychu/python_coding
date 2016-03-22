import csv
from io import StringIO

from django import forms

from core.validators import validate_tasty
from .models import Seller, Purchase, Taster, Flavor


class FlavorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FlavorForm, self).__init__(*args, **kwargs)
        self.fields['title'].validators.append(validate_tasty)
        self.fields['slug'].validators.append(validate_tasty)

    class Meta:
        model = Flavor


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


class IceCreamReviewForm(forms.Form):
    # Содержимое формы

    def clean(self):
        cleaned_data = super(TasterForm, self).clean()
        flavor = cleaned_data.get('flavor')
        age = cleaned_data.get('age')

        if flavor == 'coffee' and age < 3:
            # Запишем ошибку, которую выведем позже
            msg = 'Coffee Ice Cream is not for Babies.'
            self.add_error('flavor', msg)
            self.add_error('age', msg)

        # всегда возвращаем полный набор cleaned data
        return cleaned_data


class IceCreamOrderForm(forms.Form):
    """
    Нормально можно бы было сделать и с forms.ModelForm.
    Но мы используем forms.Form здесь для демонстрации техники,
    которую можно применить в любой форме.
    """

    slug = forms.ChoiceField('Flavor')
    toppings = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(IceCreamOrderForm, self).__init__(*args, **kwargs)

        # что то связано с перезапуском сервера,
        # вроде надо перезагрузить, если не было ранее
        self.fields['slug'].choices = [
            (x.slug, x.title) for x in Flavor.objects.all()
        ]
        # можно с фильтром, но сейчас не об этом

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Flavor.objects.get(slug=slug).scoops_remaining <= 0:
            msg = 'Извините. у нас нету такого аромата'
            raise forms.ValidationError(msg)
        return slug

    def clean(self):
        cleaned_data = super(IceCreamOrderForm, self).clean()
        slug = cleaned_data.get('slug', '')
        toppings = cleaned_data.get('toppings', '')

        # простенький пример валидации для "too much chocolate"
        if ('chocolate' in slug.lower()
            and 'chocolate' in toppings.lower()
            ):
            msg = "Ваш заказ имеет слишком много шоколада."
            raise forms.ValidationError(msg)
        return cleaned_data
