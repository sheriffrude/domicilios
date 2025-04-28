from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Servicio
from direcciones.models import Direccion
from direcciones.serializers import DireccionSerializer
from conductores.serializers import ConductorSerializer

class ServicioSerializer(serializers.ModelSerializer):
    direccion_recogida = DireccionSerializer(read_only=True)
    conductor = ConductorSerializer(read_only=True)
    
    class Meta:
        model = Servicio
        fields = '__all__'
        read_only_fields = ('solicitado', 'asignado', 'completado')

class SolicitudServicioSerializer(serializers.ModelSerializer):
    direccion = serializers.CharField(max_length=255, required=True, write_only=True)
    latitud = serializers.DecimalField(max_digits=9, decimal_places=6, required=True, write_only=True)
    longitud = serializers.DecimalField(max_digits=9, decimal_places=6, required=True, write_only=True)
    direccion_recogida_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Servicio
        fields = ('direccion', 'latitud', 'longitud', 'direccion_recogida_id', 'notas')
    
    def validate(self, data):
        if 'direccion_recogida_id' in data and any(field in data for field in ['direccion', 'latitud', 'longitud']):
            raise serializers.ValidationError("Proporciona una dirección completa O un ID de dirección, no ambos")
        
        if any(field in data for field in ['direccion', 'latitud', 'longitud']):
            if not all(field in data for field in ['direccion', 'latitud', 'longitud']):
                raise serializers.ValidationError("Debes proporcionar dirección, latitud y longitud")
        
        if 'latitud' in data:
            if not (-4.23 <= float(data['latitud']) <= 13.38):
                raise serializers.ValidationError('Latitud fuera del rango permitido para Colombia (-4.23 a 13.38)')
        
        if 'longitud' in data:
            if not (-79.00 <= float(data['longitud']) <= -66.85):
                raise serializers.ValidationError('Longitud fuera del rango permitido para Colombia (-79.00 a -66.85)')
        
        return data

class ActualizarEstadoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('estado',)