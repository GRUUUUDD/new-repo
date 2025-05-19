from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import PermissionDenied
import os

from .admin import CustomUserAdmin
from .models import CustomUser
from .middleware import RoleRedirectMiddleware
from .views import (
    ResidentDashboardView,
    SpecialistDashboardView,
    TSZHDashboardView,
    CustomLoginView,
    ReferenceView
)
User = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role=3,
            first_name="Иван",
            last_name="Петров",
            apartment=101,
            phone='+79991112233',
            avatar=SimpleUploadedFile("test.jpg", b"content")
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "Иван Петров (Жилец)")

    def test_role_properties(self):
        self.assertTrue(self.user.is_resident)
        self.assertFalse(self.user.is_specialist)
        self.assertTrue(self.user.avatar)

    def test_dashboard_url(self):
        self.assertEqual(self.user.get_dashboard_url(), 'resident_dashboard')

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Иван Петров")

class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.resident = User.objects.create_user(
            username='resident', password='testpass', role=3)
        self.specialist = User.objects.create_user(
            username='specialist', password='testpass', role=4)
        self.tszh = User.objects.create_user(
            username='tszh', password='testpass', role=2)

    def test_dashboard_access(self):
        # Жилец
        self.client.force_login(self.resident)
        response = self.client.get(reverse('resident_dashboard'))
        self.assertEqual(response.status_code, 200)

        # Специалист
        self.client.force_login(self.specialist)
        response = self.client.get(reverse('specialist_dashboard'))
        self.assertEqual(response.status_code, 200)

        # ТСЖ
        self.client.force_login(self.tszh)
        response = self.client.get(reverse('tszh_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_reference_view(self):
        self.client.force_login(self.resident)
        response = self.client.get(reverse('reference'))
        self.assertContains(response, 'Устав ТСЖ')

class MixinsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.resident = User.objects.create_user(
            username='resident', password='testpass', role=3)
        self.tszh = User.objects.create_user(
            username='tszh', password='testpass', role=2)

    def test_resident_mixin(self):
        request = self.factory.get('/')
        request.user = self.resident
        response = ResidentDashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)