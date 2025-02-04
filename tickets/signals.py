# tickets/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import TicketHistory

@receiver(post_save, sender=TicketHistory)
def send_ticket_update_email(sender, instance, created, **kwargs):
    if created and instance.status:
        ticket = instance.ticket
        subject = f"Atualização do Ticket #{ticket.id}: {instance.status}"
        message = f"""
Olá,

O ticket #{ticket.id} teve uma atualização.

Comentário: {instance.comment}
Novo status: {instance.status}

Acesse a plataforma para mais detalhes.
"""
        # Envia para o usuário que criou o ticket; personalize conforme necessário
        recipient_list = [ticket.created_by.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
