# domicilios
Prueba técnica para Alfred como desarrollador Backend Senior

# Domicilios - API de Gestión de Servicios de Transporte


API para gestión de servicios de domicilio que permite la asignación automática del conductor más cercano disponible a la ubicación del cliente.

---

## Características principales

- Gestión completa de Direcciones (CRUD)
- Gestión completa de Conductores (CRUD)
- Solicitud y asignación automática de servicios
- Cálculo de distancias y tiempos estimados de llegada
- Autenticación mediante tokens
- Docker y Docker Compose para facilitar el despliegue

---

## Estructura del proyecto

- `direcciones`: Gestión de ubicaciones
- `conductores`: Gestión de conductores y sus vehículos
- `servicios`: Gestión del ciclo de vida de los servicios
- `autenticacion`: Manejo de registro y autenticación

---

## Requisitos previos

- Docker y Docker Compose
- Git

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/yourusername/domicilios.git
cd domicilios
```

### 2. Configuración de variables de entorno

Copiar el archivo de ejemplo `.env.example` a `.env`:

```bash
cp domicilios/.env.example domicilios/.env
```

Editar el archivo `.env` con tus propias credenciales:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=domiciliosdb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

> **IMPORTANTE**: Necesitarás una clave de API de Google Maps con los servicios de Distance Matrix habilitados.

---

### 3. Levantar los servicios con Docker Compose

```bash
cd domicilios
docker-compose up --build
```

La aplicación estará disponible en:  
👉 `http://localhost:8000/`

---

## Datos de prueba iniciales

Al iniciar la aplicación, se generan automáticamente:
- 20 direcciones aleatorias en Bogotá
- 20 conductores con sus respectivos vehículos
- Un usuario administrador:

| Usuario  | Contraseña |
|----------|------------|
| admin    | admin123   |

---

## Problemas para ingresar al panel de administración

En caso de que no puedas ingresar al panel de administración (`/admin`) usando las credenciales predeterminadas (`admin` / `admin123`), es posible que el superusuario no se haya creado correctamente.

Para crear manualmente un superusuario:

```bash
docker-compose exec web python manage.py createsuperuser
```

Sigue las instrucciones para definir el `username`, `email` y `password` del nuevo administrador.

---

## Resetear la base de datos en desarrollo

Si prefieres reiniciar la base de datos desde cero (eliminando todos los datos anteriores), puedes hacerlo con:

```bash
docker-compose down -v
docker-compose up --build
```

Esto eliminará el volumen de datos de PostgreSQL, regenerará la base de datos, y ejecutará nuevamente el script de carga de datos iniciales.

---

## Uso de la API

### Autenticación

Todas las rutas de la API requieren autenticación mediante token, excepto el registro de usuarios.

#### Registro de usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevouser",
    "password": "password123",
    "password2": "password123",
    "email": "user@example.com",
    "first_name": "Nombre",
    "last_name": "Apellido"
  }'
```

#### Obtener token de autenticación

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevouser",
    "password": "password123"
  }'
```

---

### Endpoints principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/direcciones/` | GET | Listar direcciones |
| `/api/direcciones/` | POST | Crear dirección |
| `/api/conductores/` | GET | Listar conductores |
| `/api/conductores/{id}/actualizar_ubicacion/` | PATCH | Actualizar ubicación del conductor |
| `/api/conductores/{id}/actualizar_estado/` | PATCH | Actualizar estado del conductor |
| `/api/servicios/` | POST | Solicitar un servicio |
| `/api/servicios/{id}/completar_servicio/` | PATCH | Marcar servicio como completado |

Para ejemplos detallados de uso, consulta el script de prueba: `scripts/test_api.py`

---

### Ejemplo de solicitud de servicio

Para solicitar un servicio usando una dirección existente:

```bash
curl -X POST http://localhost:8000/api/servicios/ \
  -H "Authorization: Token tu-token-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "direccion_recogida_id": 1,
    "notas": "Por favor, llegar puntual"
  }'
```

O creando una nueva dirección:

```bash
curl -X POST http://localhost:8000/api/servicios/ \
  -H "Authorization: Token tu-token-aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "direccion": "Calle 100 #15-20, Bogotá",
    "latitud": 4.6871,
    "longitud": -74.0436,
    "notas": "Edificio azul"
  }'
```

---

## Lógica de asignación de conductores

La API asigna conductores siguiendo este proceso:

1. Busca conductores disponibles.
2. Calcula la distancia y tiempo usando Google Maps Distance Matrix API.
3. Si Google Maps falla, utiliza fórmula Haversine para calcular distancia.
4. Asigna el conductor más cercano al cliente.
5. Actualiza el estado del conductor a "ocupado".

---

## Pruebas

Para ejecutar los tests unitarios:

```bash
docker-compose run web python manage.py test
```

---

## Despliegue en la nube (AWS)

### Servicios recomendados

- **EC2** o **Elastic Beanstalk** para hospedar la app Django
- **RDS PostgreSQL** como base de datos
- **ElastiCache** para caché
- **Secrets Manager** para gestionar credenciales
- **CloudWatch** para monitoreo y logs
- **CloudFront** como CDN
- **Load Balancer** (ELB) para balanceo de carga
- **Route 53** para DNS

### Justificación

#### Escalabilidad
- Autoescalado en EC2
- Separación de servicios
- Uso de SQS para tareas asíncronas

#### Seguridad
- WAF para protección
- VPC privadas
- HTTPS obligatorio
- Secrets Manager para credenciales

---

## Consideraciones futuras

- Implementar WebSockets para actualizaciones en tiempo real.
- Seguimiento de conductores en vivo.
- Sistema de calificaciones para conductores y usuarios.
- Integración de pagos online.
- Soporte para viajes múltiples (multi-dirección).

---

## Licencia

Este proyecto es privado y confidencial.

---

## Contacto

Para preguntas o soporte: [sheriffrude@gmail.com]
