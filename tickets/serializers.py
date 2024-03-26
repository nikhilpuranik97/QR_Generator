from rest_framework import serializers
from .models import TicketQR

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketQR
        fields = '__all__'