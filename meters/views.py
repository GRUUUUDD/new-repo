from django.views.generic import FormView
from .models import Tariff
from .forms import PaymentCalcForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.pdfbase import pdfmetrics  # Правильный импорт pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont  # Импорт TTFont
import os


def generate_pdf(request):
    try:
        # Путь к шрифту (убедитесь, что файл arial.ttf существует)
        font_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static',
            'fonts',
            'arial.ttf'
        )

        # Проверка существования файла шрифта
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Файл шрифта не найден: {font_path}")

        # Регистрация шрифта
        pdfmetrics.registerFont(TTFont('Arial', font_path))

        # Создание PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        # Установка русского шрифта
        p.setFont("Arial", 14)

        # Добавление текста
        text_lines = [
            (20 * mm, 270 * mm, "Квитанция ТСЖ"),
            (20 * mm, 260 * mm, f"Жилец: {request.user.get_full_name()}"),
            (20 * mm, 250 * mm, "Адрес: ул. Примерная, д. 1, кв. 1"),
            (20 * mm, 230 * mm, "Услуга:"),
            (70 * mm, 230 * mm, "Количество:"),
            (120 * mm, 230 * mm, "Сумма:"),
            (20 * mm, 220 * mm, "Холодная вода"),
            (70 * mm, 220 * mm, "10 м³"),
            (120 * mm, 220 * mm, "450 руб")
        ]

        for x, y, text in text_lines:
            p.drawString(x, y, text)

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"Ошибка при генерации PDF: {str(e)}", status=500)



class PaymentCalcView(LoginRequiredMixin, FormView):
    template_name = 'meters/calculation.html'
    form_class = PaymentCalcForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tariffs'] = Tariff.objects.all()
        return context

    def form_valid(self, form):
        # Здесь будет логика расчета
        return self.render_to_response(
            self.get_context_data(form=form)
        )
