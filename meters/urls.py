from django.urls import path
from .views import PaymentCalcView
from . import views

urlpatterns = [
    path('calc/', PaymentCalcView.as_view(), name='payment_calc'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]