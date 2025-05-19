from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.price} руб/{self.unit}"


class MeterReading(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tariff = models.ForeignKey('Tariff', on_delete=models.CASCADE)  # Используем строковую ссылку
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']  # Сортировка по дате (новые сначала)

    @property
    def cost(self):
        return self.value * self.tariff.price

    def __str__(self):
        return f"Показание {self.user.username} - {self.tariff.name}"