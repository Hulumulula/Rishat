from django import forms


ITEM_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddItemForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=ITEM_QUANTITY_CHOICES,
        coerce=int,
        label='',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

