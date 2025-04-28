from django.db import models

class Direccion(models.Model):
    direccion = models.CharField(max_length=255)  
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        
        if not ( -4.23 <= float(self.latitud) <= 13.38 ):
            raise ValidationError('Latitud fuera del rango permitido para Colombia (-4.23 a 13.38)')
        if not ( -79.00 <= float(self.longitud) <= -66.85 ):
            raise ValidationError('Longitud fuera del rango permitido para Colombia (-79.00 a -66.85)')

    def __str__(self):
        return f"{self.direccion} ({self.latitud}, {self.longitud})"
