# Booking System API

REST API para gestión de reservas de canchas deportivas, construida con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Bcrypt (password hashing)

## Funcionalidades

- Registro e inicio de sesión de usuarios con JWT
- Gestión de canchas deportivas (CRUD)
- Gestión de reservas con autenticación

## Endpoints

### Auth
- `POST /auth/signup` — Registro de usuario
- `POST /auth/login` — Login (retorna JWT token)
- `GET /auth/users/me` — Info del usuario logueado

### Courts
- `GET /courts` — Listar todas las canchas
- `GET /courts/{id}` — Obtener cancha por ID
- `POST /courts` — Crear cancha

### Bookings
- `POST /bookings` — Crear reserva (requiere auth)
- `GET /bookings` — Listar todas las reservas
- `GET /bookings/{id}` — Obtener reserva por ID

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno virtual: `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Crear archivo `.env` con tu `DATABASE_URL`
6. Ejecutar: `uvicorn main:app --reload`

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_db
SECRET_KEY=tu_clave_secreta
```