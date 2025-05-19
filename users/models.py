from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        (1, 'Глава ТСЖ'),
        (2, 'Член ТСЖ'),
        (3, 'Жилец'),
        (4, 'Специалист'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)  # Добавлен default
    phone = models.CharField(max_length=20, blank=True)  # Добавлен blank=True
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Адрес для жильцов и членов ТСЖ
    entrance = models.PositiveIntegerField(blank=True, null=True)
    apartment = models.PositiveIntegerField(blank=True, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)

    # Профессия для специалистов
    profession = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    @property
    def is_resident(self):
        return self.role == 3  # Жилец

    @property
    def is_specialist(self):
        return self.role == 4  # Специалист

    @property
    def is_tszh_member(self):
        return self.role in [1, 2]  # Глава ТСЖ или член ТСЖ

    def get_dashboard_url(self):
        if self.role in [1, 2]:  # ТСЖ
            return 'tszh_dashboard'
        elif self.role == 3:  # Жилец
            return 'resident_dashboard'
        elif self.role == 4:  # Специалист
            return 'specialist_dashboard'
        return 'login'  # fallback
