from django import forms
from .models import Tariff

class PaymentCalcForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tariffs = Tariff.objects.all()
        for tariff in tariffs:
            self.fields[f'tariff_{tariff.id}'] = forms.DecimalField(
                label=f"{tariff.name} ({tariff.unit})",
                required=True,
                min_value=0,
                max_digits=10,
                decimal_places=2
            )