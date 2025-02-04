# tickets/forms.py
from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['priority', 'category', 'description', 'status']
