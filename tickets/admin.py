# tickets/admin.py
from django.contrib import admin
from .models import Company, UserProfile, Ticket, TicketHistory, TicketAttachment

admin.site.register(Company)
admin.site.register(UserProfile)
admin.site.register(Ticket)
admin.site.register(TicketHistory)
admin.site.register(TicketAttachment)
