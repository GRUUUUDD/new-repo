from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Tariff, MeterReading
from .forms import PaymentCalcForm
from django.utils import timezone
import os

User = get_user_model()


class ModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Иван",
            last_name="Петров"
        )

        self.tariff = Tariff.objects.create(
            name="Холодная вода",
            price=45.00,
            unit="м³"
        )

        self.reading = MeterReading.objects.create(
            user=self.user,
            tariff=self.tariff,
            value=10.00
        )

    # Тест 1: Проверка расчета стоимости показания
    def test_reading_cost_property(self):
        self.assertEqual(self.reading.cost, 450.00)  # 10 * 45 = 450

    # Тест 2: Проверка сортировки показаний
    def test_reading_ordering(self):
        # Создаем первое показание с вчерашней датой
        self.reading.date = timezone.now() - timezone.timedelta(days=1)
        self.reading.save()

        # Создаем новое показание с текущей датой
        new_reading = MeterReading.objects.create(
            user=self.user,
            tariff=self.tariff,
            value=15.00,
            date=timezone.now()  # Явно задаем дату
        )
        readings = MeterReading.objects.all()
        self.assertEqual(readings[0], new_reading)  # Теперь новый объект будет первым

class FormsTests(TestCase):
    def setUp(self):
        Tariff.objects.create(name="Электричество", price=5.50, unit="кВт·ч")
        Tariff.objects.create(name="Горячая вода", price=80.00, unit="м³")

    # Тест 3: Динамическое создание полей формы
    def test_form_field_generation(self):
        form = PaymentCalcForm()
        self.assertIn('tariff_1', form.fields)  # Проверяем наличие полей
        self.assertIn('tariff_2', form.fields)

    # Тест 4: Валидация отрицательных значений
    def test_form_validation(self):
        data = {'tariff_1': -5, 'tariff_2': 10}
        form = PaymentCalcForm(data)
        self.assertFalse(form.is_valid())

class AdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            password="adminpass",
            email="admin@example.com"
        )
        self.client.login(username="admin", password="adminpass")
        self.tariff = Tariff.objects.create(name="Газ", price=7.00, unit="м³")

    # Тест 5: Проверка отображения тарифов в админке
    def test_tariff_admin_listing(self):
        url = reverse('admin:meters_tariff_changelist')
        response = self.client.get(url)
        self.assertContains(response, "Газ")