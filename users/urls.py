from django.urls import path
from .views import CustomLoginView
from .views import ResidentDashboardView, SpecialistDashboardView, TSZHDashboardView
from .views import ReferenceView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('resident/', ResidentDashboardView.as_view(), name='resident_dashboard'),
    path('specialist/', SpecialistDashboardView.as_view(), name='specialist_dashboard'),
    path('tszh/', TSZHDashboardView.as_view(), name='tszh_dashboard'),
    path('reference/', ReferenceView.as_view(), name='reference'),
]




