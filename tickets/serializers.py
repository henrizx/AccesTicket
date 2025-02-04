# tickets/serializers.py
from rest_framework import serializers
from .models import Company, Ticket, TicketHistory, TicketAttachment, UserProfile
from django.contrib.auth.models import User

# Serializador para Company
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

# Serializador para o modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializador para UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

# Serializador para TicketAttachment
class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ['id', 'file', 'uploaded_at']

# Serializador para TicketHistory
class TicketHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketHistory
        fields = ['id', 'ticket', 'user', 'comment', 'status', 'created_at']

# Serializador para Ticket
class TicketSerializer(serializers.ModelSerializer):
    histories = TicketHistorySerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
