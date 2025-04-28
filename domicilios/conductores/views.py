from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conductor
from .serializers import ConductorSerializer, ConductorUbicacionSerializer

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'])
    def actualizar_ubicacion(self, request, pk=None):
        conductor = self.get_object()
        serializer = ConductorUbicacionSerializer(conductor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def actualizar_estado(self, request, pk=None):
        conductor = self.get_object()
        estado = request.data.get('estado')
        if estado not in [choice[0] for choice in Conductor.ESTADOS_CHOICES]:
            return Response({'estado': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)
        conductor.estado = estado
        conductor.save()
        return Response({'estado': conductor.estado})
