from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .mixins import ResidentRequiredMixin, SpecialistRequiredMixin, TSZHMemberRequiredMixin
from django.urls import reverse_lazy  # Изменили reverse на reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


class ResidentDashboardView(ResidentRequiredMixin, TemplateView):
    template_name = 'users/dashboards/resident.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте данные для жильца
        return context


class SpecialistDashboardView(SpecialistRequiredMixin, TemplateView):
    template_name = 'users/dashboards/specialist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте данные для специалиста
        return context


class TSZHDashboardView(TSZHMemberRequiredMixin, TemplateView):
    template_name = 'users/dashboards/tszh.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context




class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 1 or user.role == 2:  # ТСЖ
            return reverse_lazy('tszh_dashboard')
        elif user.role == 3:  # Жилец
            return reverse_lazy('resident_dashboard')
        elif user.role == 4:  # Специалист
            return reverse_lazy('specialist_dashboard')
        return reverse_lazy('forum')  # Или другой URL по умолчанию


class ReferenceView(LoginRequiredMixin, TemplateView):
    template_name = 'users/reference.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = [
            {
                'title': 'Документы',
                'items': [
                    {'name': 'Устав ТСЖ', 'url': '/documents/ustav.pdf'},
                    {'name': 'Правила дома', 'url': '/documents/rules.pdf'}
                ]
            }
        ]
        return context


def health_check(request):
    return HttpResponse("🟢 It works!")