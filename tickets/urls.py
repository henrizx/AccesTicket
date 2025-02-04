# tickets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, TicketViewSet, TicketHistoryViewSet, TicketAttachmentViewSet,
    listar_tickets, ticket_detail, ticket_form, register
)
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'ticket-histories', TicketHistoryViewSet)
router.register(r'ticket-attachments', TicketAttachmentViewSet)

urlpatterns = [
    # Endpoints da API
    path('api/', include(router.urls)),

    # Rotas para o site
    path('', listar_tickets, name='listar_tickets'),
    path('ticket/<int:pk>/', ticket_detail, name='ticket_detail'),
    path('ticket/novo/', ticket_form, name='ticket_create'),
    path('ticket/<int:pk>/editar/', ticket_form, name='ticket_edit'),

    # Autenticação: Login, Logout e Registro
    path('login/', auth_views.LoginView.as_view(template_name='tickets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]
