from django import forms



EQUIPMENT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddEquipmentForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=EQUIPMENT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)




class CouponForm(forms.Form):
    code = forms.CharField()