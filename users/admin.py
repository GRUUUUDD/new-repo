from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_role_display', 'phone', 'apartment', 'floor', 'entrance', 'profession')
    search_fields = ('username', 'email', 'phone', 'apartment')
    ordering = ('username',)

# Регистрация кастомной модели
admin.site.register(CustomUser, CustomUserAdmin)