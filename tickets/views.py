from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm

@login_required
def create_ticket(request):
    # ТОЛЬКО жильцы могут создавать заявки
    if request.user.role != 3:
        messages.error(request, "Доступ запрещен.")
        return redirect('home')

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.author = request.user
            ticket.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('tickets:history')
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def ticket_history(request):
    # Жильцы видят отправленные заявки, остальные — входящие
    if request.user.role == 3:
        tickets = Ticket.objects.filter(author=request.user)
    else:
        tickets = Ticket.objects.filter(receiver=request.user)
    return render(request, 'tickets/history.html', {'tickets': tickets})

@login_required
def update_status(request, ticket_id, new_status):
    # Менять статус может только получатель
    ticket = Ticket.objects.get(id=ticket_id)
    if request.user == ticket.receiver:
        ticket.status = new_status
        ticket.save()
        messages.success(request, "Статус обновлен!")
    else:
        messages.error(request, "Доступ запрещен.")
    return redirect('tickets:history')

@login_required
def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    # Проверка прав: только автор или получатель могут смотреть заявку
    if request.user != ticket.author and request.user != ticket.receiver:
        messages.error(request, "Доступ запрещен.")
        return redirect('tickets:history')
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})