from django.shortcuts import render
import os
import googlemaps
from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Servicio
from .serializers import ServicioSerializer, SolicitudServicioSerializer, ActualizarEstadoServicioSerializer
from conductores.models import Conductor
from direcciones.models import Direccion
from math import radians, cos, sin, asin, sqrt
from rest_framework.exceptions import ValidationError, APIException

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all().select_related(
        'direccion_recogida', 
        'conductor', 
        'conductor__usuario',
        'cliente'
    )
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return SolicitudServicioSerializer
        if self.action in ['update_status', 'actualizar_estado']:
            return ActualizarEstadoServicioSerializer
        return ServicioSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        

        direccion_recogida = self._obtener_direccion_recogida(serializer.validated_data)
        if not direccion_recogida:
            raise ValidationError("Debes proporcionar una dirección de recogida válida")


        self._validar_coordenadas(direccion_recogida.latitud, direccion_recogida.longitud)


        conductores_disponibles = Conductor.objects.filter(estado='disponible')
        if not conductores_disponibles.exists():
            raise ValidationError("No hay conductores disponibles en este momento")


        try:
            conductor, distancia, tiempo = self._encontrar_conductor_mas_cercano(
                conductores_disponibles, 
                direccion_recogida
            )
        except Exception as e:
            raise APIException("Error al calcular distancias: " + str(e))


        servicio_data = {
            'cliente': request.user,
            'direccion_recogida': direccion_recogida,
            'conductor': conductor,
            'estado': 'asignado',
            'asignado': timezone.now(),
            'tiempo_estimado': tiempo,
            'distancia': distancia,
            **{k: v for k, v in serializer.validated_data.items() 
               if k not in ['direccion', 'latitud', 'longitud', 'direccion_recogida_id']}
        }
        
        servicio = Servicio.objects.create(**servicio_data)
        conductor.estado = 'ocupado'
        conductor.save()

        return Response(ServicioSerializer(servicio).data, status=status.HTTP_201_CREATED)

    def _obtener_direccion_recogida(self, validated_data):
        """Obtiene o crea la dirección de recogida"""
        if 'direccion_recogida_id' in validated_data:
            try:
                return Direccion.objects.get(pk=validated_data['direccion_recogida_id'])
            except Direccion.DoesNotExist:
                raise ValidationError("Dirección de recogida no encontrada")
        
        if all(field in validated_data for field in ['direccion', 'latitud', 'longitud']):
            self._validar_coordenadas(validated_data['latitud'], validated_data['longitud'])
            return Direccion.objects.create(
                direccion=validated_data['direccion'],
                latitud=validated_data['latitud'],
                longitud=validated_data['longitud']
            )
        
        return None

    def _validar_coordenadas(self, latitud, longitud):
        """Valida que las coordenadas sean correctas"""
        if not (-90 <= latitud <= 90) or not (-180 <= longitud <= 180):
            raise ValidationError("Coordenadas geográficas inválidas")

    def _encontrar_conductor_mas_cercano(self, conductores, direccion_recogida):
        try:
            gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
            destino = (direccion_recogida.latitud, direccion_recogida.longitud)
            
 
            origins = [f"{c.latitud_actual},{c.longitud_actual}" for c in conductores]
            

            resultado = gmaps.distance_matrix(
                origins=origins,
                destinations=[f"{destino[0]},{destino[1]}"],
                mode="driving",
                units="metric",
                region="co" 
            )
            
            if resultado['status'] == 'OK':
                distancias = []
                for i, row in enumerate(resultado['rows']):
                    elemento = row['elements'][0]
                    if elemento['status'] == 'OK':
                        distancia = elemento['distance']['value'] / 1000  
                        duracion = elemento['duration']['value'] / 60    
                        distancias.append((i, distancia, duracion))
                
                if distancias:
                    i, min_dist, min_time = min(distancias, key=lambda x: x[1])
                    return conductores[i], min_dist, min_time
            
            #Haversine si Google Maps falla
            return self._haversine_conductor_mas_cercano(conductores, direccion_recogida)
            
        except Exception:

            return self._haversine_conductor_mas_cercano(conductores, direccion_recogida)

    def _haversine_conductor_mas_cercano(self, conductores, direccion_recogida):
        conductor_mas_cercano = None
        distancia_minima = float('inf')
        
        for conductor in conductores:
            distancia = self._haversine(
                conductor.latitud_actual, conductor.longitud_actual,
                direccion_recogida.latitud, direccion_recogida.longitud
            )
            
            if distancia < distancia_minima:
                distancia_minima = distancia
                conductor_mas_cercano = conductor
                
        return conductor_mas_cercano, distancia_minima, int(distancia_minima * 2)

    def _haversine(self, lat1, lon1, lat2, lon2):
       
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        
        # Fórmula Haversine
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371  # ---- (Radio de la Tierra en km) ----
        
        return c * r
        
    @action(detail=True, methods=['patch'])
    def completar_servicio(self, request, pk=None):
        servicio = self.get_object()
        
        if servicio.estado == 'completado':
            raise ValidationError("El servicio ya está completado")
            
        if servicio.estado not in ['asignado', 'en_progreso']:
            raise ValidationError("Solo servicios asignados o en progreso pueden completarse")
            
        servicio.estado = 'completado'
        servicio.completado = timezone.now()
        servicio.save()
        
        if servicio.conductor:
            servicio.conductor.estado = 'disponible'
            servicio.conductor.save()
            
        return Response(ServicioSerializer(servicio).data)
        
    @action(detail=True, methods=['patch'], url_path='actualizar-estado')
    def actualizar_estado(self, request, pk=None):
        servicio = self.get_object()
        serializer = self.get_serializer(servicio, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        nuevo_estado = serializer.validated_data.get('estado')
        
        if servicio.estado == 'completado' and nuevo_estado != 'completado':
            raise ValidationError("No se puede cambiar el estado de un servicio completado")
            
        if nuevo_estado == 'completado':
            servicio.completado = timezone.now()
            if servicio.conductor:
                servicio.conductor.estado = 'disponible'
                servicio.conductor.save()
        
        serializer.save()
        return Response(ServicioSerializer(servicio).data)