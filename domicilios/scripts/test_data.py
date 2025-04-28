import os
import sys
import django
import random
from faker import Faker
from faker_vehicle import VehicleProvider

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domicilios.settings')
django.setup()

from django.contrib.auth.models import User
from direcciones.models import Direccion
from conductores.models import Conductor
from servicios.models import Servicio  

def create_test_data(num_direcciones=20, num_conductores=20):
    fake = Faker('es_CO')  
    fake.add_provider(VehicleProvider)
    

    barrios_bogota = [
        "Chapinero", "Usaquén", "Suba", "Kennedy", "Teusaquillo", 
        "Fontibón", "La Candelaria", "Santa Fe", "Engativá", "Bosa",
        "Ciudad Bolívar", "San Cristóbal", "Puente Aranda", "Los Mártires", 
        "Barrios Unidos"
    ]
    
    tipos_via = ["Calle", "Carrera", "Diagonal", "Transversal", "Avenida"]
    
    print(f"Generando {num_direcciones} direcciones en Bogotá...")
    
    print("Eliminando servicios existentes...")
    Servicio.objects.all().delete()
    
    print("Eliminando direcciones y conductores existentes...")
    Direccion.objects.all().delete()
    Conductor.objects.all().delete()
    
    for _ in range(num_direcciones):
        lat = round(random.uniform(4.48, 4.82), 6) 
        lng = round(random.uniform(-74.22, -73.99), 6)
        
        tipo_via = random.choice(tipos_via)
        numero_via = random.randint(1, 170)
        complemento = f"# {random.randint(1, 150)}-{random.randint(1, 99)}"
        barrio = random.choice(barrios_bogota)
        
        direccion_completa = f"{tipo_via} {numero_via} {complemento}, {barrio}, Bogotá"

        Direccion.objects.create(
            direccion=direccion_completa,
            latitud=lat,
            longitud=lng
        )
    
    print(f"Generando {num_conductores} conductores en Bogotá...")

    marcas_vehiculos = [
        "Renault Logan", "Chevrolet Spark", "Kia Picanto", "Mazda 2", 
        "Nissan Versa", "Toyota Corolla", "Hyundai i10", "Renault Sandero", 
        "Chevrolet Beat", "Nissan March"
    ]

    for i in range(num_conductores):
        username = f"driver{i+1}"

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )


        lat = round(random.uniform(4.48, 4.82), 6)
        lng = round(random.uniform(-74.22, -73.99), 6)
        
        letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        numeros = ''.join(random.choices('0123456789', k=3))
        placa_colombiana = f"{letras}{numeros}"

        Conductor.objects.create(
            usuario=user,
            placa=placa_colombiana,
            modelo=random.choice(marcas_vehiculos),
            año=random.randint(2010, 2023),
            latitud_actual=lat,
            longitud_actual=lng,
            estado=random.choice(['disponible', 'ocupado', 'no disponible']),
            clasificacion=round(random.uniform(3.0, 5.0), 1) 
        )

    print("Datos de prueba para Bogotá generados exitosamente.")
    print(f"- {num_direcciones} direcciones creadas en Bogotá")
    print(f"- {num_conductores} conductores creados en Bogotá")
    print("Usuario admin creado con username: admin, password: admin123")

if __name__ == "__main__":
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")

    create_test_data(num_direcciones=20, num_conductores=20)