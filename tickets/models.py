# tickets/models.py
from django.db import models
from django.contrib.auth.models import User

# Modelo para as Empresas
class Company(models.Model):
    name = models.CharField("Nome", max_length=255)
    cnpj = models.CharField("CNPJ", max_length=20, unique=True)
    address = models.CharField("Endereço", max_length=255)
    phone = models.CharField("Telefone", max_length=20)
    email = models.EmailField("E-mail", unique=True)
    active = models.BooleanField("Ativo", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return self.name

# Definição dos papéis para os usuários
ROLE_CHOICES = (
    ('admin', 'Administrador'),
    ('manager', 'Gestor'),
    ('technician', 'Técnico'),
    ('user', 'Usuário Final'),
)

# Perfil do usuário (extensão do modelo User)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    role = models.CharField("Função", max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.user.username

# Opções de prioridade e status para os tickets
PRIORITY_CHOICES = (
    ('alta', 'Alta'),
    ('media', 'Média'),
    ('baixa', 'Baixa'),
)

STATUS_CHOICES = (
    ('aberto', 'Aberto'),
    ('em_andamento', 'Em andamento'),
    ('pendente', 'Pendente'),
    ('resolvido', 'Resolvido'),
    ('fechado', 'Fechado'),
)

# Modelo do Ticket
class Ticket(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tickets')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets_created')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_assigned')
    priority = models.CharField("Prioridade", max_length=20, choices=PRIORITY_CHOICES, default='media')
    category = models.CharField("Categoria", max_length=50, blank=True, null=True,
                                help_text="Ex.: Hardware, Software, Rede, Acesso")
    description = models.TextField("Descrição do Problema")
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='aberto')
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def __str__(self):
        return f'Ticket #{self.id} - {self.status}'

# Histórico de atualizações (comentários e mudanças de status)
class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='histories')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField("Comentário", blank=True, null=True)
    status = models.CharField("Status Atualizado", max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        return f'Histórico do Ticket #{self.ticket.id} por {self.user}'

# Anexos para os tickets (ex.: imagens, logs)
class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField("Arquivo", upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField("Enviado em", auto_now_add=True)

    def __str__(self):
        return f'Anexo do Ticket #{self.ticket.id}'
