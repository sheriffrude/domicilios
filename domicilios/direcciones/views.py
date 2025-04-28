from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Direccion
from .serializers import DireccionSerializer


# CRUDD
class DireccionViewSet(viewsets.ModelViewSet):
    
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]
