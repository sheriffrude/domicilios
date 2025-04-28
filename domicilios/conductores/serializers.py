from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conductor

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ConductorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Conductor
        fields = '__all__'
        read_only_fields = ('creado_en', 'actualizado_en')

class ConductorUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = ('id', 'latitud_actual', 'longitud_actual', 'estado')
