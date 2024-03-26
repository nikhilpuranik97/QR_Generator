from rest_framework import viewsets
from .models import TicketQR
from .serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = TicketQR.objects.all()
    serializer_class = TicketSerializer
