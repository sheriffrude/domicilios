#Script para testear la API de servicios de domicilio.
#Ejecutar con: python scripts/test_api.py


import os
import sys
import django
import requests
import json
from pprint import pprint


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'domicilios.settings')
django.setup()

API_URL = "http://localhost:8000/api"

def register_user():
    url = f"{API_URL}/auth/register/"
    data = {
        "username": "testuser",
        "password": "testpassword123",
        "password2": "testpassword123",
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(url, json=data)
    print("Registro de usuario:")
    pprint(response.json())
    return response.json()

def get_auth_token():
    url = f"{API_URL}/auth/token/"
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    print("\nToken de autenticación:")
    pprint(result)
    return result.get("token")

def list_direcciones(token):
    url = f"{API_URL}/direcciones/"
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    print("\nListado de direcciones:")
    pprint(result[:2]) 
    print(f"Total de direcciones: {len(result)}")
    return result

def list_conductores(token):
    url = f"{API_URL}/conductores/"
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(url, headers=headers)
    result = response.json()
    print("\nListado de conductores:")
    pprint(result[:2])  
    print(f"Total de conductores: {len(result)}")
    return result

def request_service(token, address_id):
    url = f"{API_URL}/servicios/"
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    data = {
        "pickup_address_id": address_id,
        "notes": "Servicio de prueba desde script"
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("\nSolicitud de servicio:")
    pprint(response.json())
    return response.json()

def complete_service(token, service_id):
    url = f"{API_URL}/servicios/{service_id}/complete_service/"
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.patch(url, headers=headers)
    print("\nServicio completado:")
    pprint(response.json())
    return response.json()

def main():
    print("===>>> PRUEBA DE LA API DE SERVICIOS DE DOMICILIO <<<===\n")
    
    try:
        register_user()
    except Exception as e:
        print(f"Error al registrar usuario o usuario ya existe: {e}")
    
    token = get_auth_token()
    if not token:
        print("Error: No se pudo obtener el token de autenticación.")
        return
    
    direcciones = list_direcciones(token)
    conductores = list_conductores(token)
    
    if direcciones and len(direcciones) > 0:
        address_id = direcciones[0]["id"]
        service = request_service(token, address_id)
        
        if service and "id" in service:
            service_id = service["id"]
            complete_service(token, service_id)
    
    print("\n=== FIN DE LA PRUEBA ===")

if __name__ == "__main__":
    main()