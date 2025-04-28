from django.db import models
from django.contrib.auth.models import User
from direcciones.models import Direccion
from conductores.models import Conductor

class Servicio(models.Model):
    
    ESTADOS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('en progreso', 'En progreso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicios_cliente')
    direccion_recogida = models.ForeignKey(
        Direccion, 
        on_delete=models.PROTECT, 
        related_name='servicios_recogida'
    )
    conductor = models.ForeignKey(
        Conductor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='servicios'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')
    solicitado = models.DateTimeField(auto_now_add=True)
    asignado = models.DateTimeField(null=True, blank=True)
    completado = models.DateTimeField(null=True, blank=True)
    tiempo_estimado = models.IntegerField(
        help_text="Tiempo estimado de llegada en minutos",
        null=True,
        blank=True
    )
    distancia = models.FloatField(
        help_text="Distanvcia en kilómetros",
        null=True,
        blank=True
    )
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Servicio---> #{self.id} - {self.get_estado_display()}"
    
    class Meta:
        ordering = ['solicitado']
