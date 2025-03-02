from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "city",
            "street",
            "house_number",
            "apartament_number",
            "postal_code",
        ]
