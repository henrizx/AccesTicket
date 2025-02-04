# tickets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Imports para as classes genéricas (se preferir)
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Company, Ticket, TicketHistory, TicketAttachment
from .serializers import CompanySerializer, TicketSerializer, TicketHistorySerializer, TicketAttachmentSerializer

# ----- API Views (ViewSets) -----

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['company__id', 'priority', 'status', 'category']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'category']

    def perform_create(self, serializer):
        # Define a empresa com base no perfil do usuário (se existir)
        company = None
        if hasattr(self.request.user, 'profile'):
            company = self.request.user.profile.company
        serializer.save(created_by=self.request.user, company=company)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        # Endpoint para adicionar comentário ou atualizar status
        ticket = self.get_object()
        comment = request.data.get('comment', '')
        status = request.data.get('status', None)
        history = TicketHistory.objects.create(
            ticket=ticket,
            user=request.user,
            comment=comment,
            status=status
        )
        serializer = TicketHistorySerializer(history)
        return Response(serializer.data)

class TicketHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketHistory.objects.all().order_by('-created_at')
    serializer_class = TicketHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TicketAttachmentViewSet(viewsets.ModelViewSet):
    queryset = TicketAttachment.objects.all()
    serializer_class = TicketAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.request.data.get('ticket')
        serializer.save(ticket_id=ticket_id)

# ----- Web Views (Templates) -----

# Página inicial que lista os tickets
@login_required
def listar_tickets(request):
    # Se o usuário possuir perfil com empresa, filtramos; caso contrário, listamos todos os tickets
    if hasattr(request.user, 'profile') and request.user.profile.company:
        tickets = Ticket.objects.filter(company=request.user.profile.company)
    else:
        tickets = Ticket.objects.all()
    return render(request, 'tickets/index.html', {'tickets': tickets})

# Detalhe do ticket, incluindo o histórico
@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

# Formulário para criação e edição de ticket
@login_required
def ticket_form(request, pk=None):
    ticket = None
    if pk:
        ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        priority = request.POST.get('priority')
        category = request.POST.get('category')
        description = request.POST.get('description')
        status = request.POST.get('status')
        if ticket:
            ticket.priority = priority
            ticket.category = category
            ticket.description = description
            ticket.status = status
            ticket.save()
            messages.success(request, "Ticket atualizado com sucesso!")
        else:
            company = request.user.profile.company if hasattr(request.user, 'profile') else None
            Ticket.objects.create(
                company=company,
                created_by=request.user,
                priority=priority,
                category=category,
                description=description,
                status='aberto'
            )
            messages.success(request, "Ticket criado com sucesso!")
        return redirect('listar_tickets')
    return render(request, 'tickets/ticket_form.html', {'ticket': ticket})

# Registro de usuário
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        company_id = request.POST.get('company')  # Empresa selecionada
        if username and password:
            from django.contrib.auth.models import User
            user = User.objects.create_user(username=username, email=email, password=password)
            # Associa o perfil ao usuário
            from .models import Company, UserProfile
            company = Company.objects.filter(id=company_id).first() if company_id else None
            UserProfile.objects.create(user=user, company=company)
            login(request, user)
            messages.success(request, "Registrado com sucesso!")
            return redirect('listar_tickets')
    companies = Company.objects.all()
    return render(request, 'tickets/register.html', {'companies': companies})

# As views de login e logout usarão as views padrão do Django
