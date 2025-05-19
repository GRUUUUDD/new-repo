from django import forms
from .models import Ticket
from users.models import CustomUser

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['receiver', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Опишите проблему...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Фильтр получателей: только ТСЖ и специалисты
        self.fields['receiver'].queryset = CustomUser.objects.filter(role__in=[1, 2, 4])
        self.fields['receiver'].label = "Кому адресована заявка"
        self.fields['description'].label = "Описание проблемы"
        self.fields['photo'].label = "Фотография (необязательно)"