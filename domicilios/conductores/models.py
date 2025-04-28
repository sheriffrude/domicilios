from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Conductor(models.Model):
    ESTADOS_CHOICES = (
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('no disponible', 'No disponible'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='conductor')
    placa = models.CharField(max_length=20)
    modelo = models.CharField(max_length=100)
    año = models.PositiveIntegerField()
    latitud_actual = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitud entre -90 y 90"
    )
    longitud_actual = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitud entre -180 y 180"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='disponible')
    clasificacion = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        help_text="Clasificación entre 0 y 5 estrellas"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.placa}"
    
    def obtener_ubicacion(self):
        return {
            'latitud': self.latitud_actual,
            'longitud': self.longitud_actual
        }
    
    def esta_disponible(self):
        return self.estado == 'disponible'
