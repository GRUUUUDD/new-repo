from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('create/', views.create_ticket, name='create'),
    path('history/', views.ticket_history, name='history'),
    path('update/<int:ticket_id>/<str:new_status>/', views.update_status, name='update_status'),
    path('detail/<int:ticket_id>/', views.ticket_detail, name='detail'),
]