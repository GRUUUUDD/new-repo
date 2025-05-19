from django.contrib import admin
from .models import Tariff, MeterReading

admin.site.register(Tariff)
admin.site.register(MeterReading)
