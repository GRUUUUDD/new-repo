from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'receiver', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('author__username', 'receiver__username')
