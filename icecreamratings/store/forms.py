from django import forms

from .models import IceCreamStore


class IceCreamStoreCreateForm(forms.ModelForm):

    class Meta:
        model = IceCreamStore
        fields = ('title', 'block_address',)


class IceCreamStoreUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # вызываем оригинальный метод __init__
        # до переназначения полей.
        super(IceCreamStoreUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = True
        self.fields['description'].required = True

    class Meta(IceCreamStoreCreateForm.Meta):
        # Показать все поля.
        fields = ('title', 'block_address', 'phone', 'description',)
