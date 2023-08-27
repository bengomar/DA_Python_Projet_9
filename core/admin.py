from django.contrib import admin
from core.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ticket, TicketAdmin)
