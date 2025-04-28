from rest_framework import serializers

from .models import Direccion

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')