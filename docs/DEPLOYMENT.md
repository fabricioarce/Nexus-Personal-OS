# Guía de Despliegue (Render / Railway)

Esta guía detalla los pasos para desplegar "Nexus Personal OS" (Backend FastAPI) en la nube y preparar el Frontend (Astro) para integración móvil.

## Arquitectura de Despliegue

Para cumplir con el objetivo de **gratuidad** y **disponibilidad 24/7 de la API**, utilizaremos la siguiente arquitectura:

1.  **Backend (API + Base de Datos)**: Alojado en **Render** (Free Tier) o **Railway**.
    *   *Por qué*: Necesitamos que la API esté viva siempre para que la App Móvil pueda consultar y guardar datos, incluso si tu PC está apagada.
    *   *Base de Datos*: **PostgreSQL** (gestionada por la plataforma). SQLite no se recomienda en la nube porque los datos se borran con cada reinicio.

2.  **Frontend (App Móvil)**: Empaquetado con **Capacitor** e instalado en tu teléfono.
    *   *Por qué*: No requiere hosting web. Los archivos HTML/JS/CSS viven dentro de la app en tu teléfono. Funciona rápido y no gasta ancho de banda descargando la interfaz.

---

## Parte 1: El Backend en la Nube

### 1. Dockerfile (Raíz del proyecto)
Crea un archivo llamado `Dockerfile` en `/home/fabri/Documents/Diario/Dockerfile`:

```dockerfile
# Dockerfile optimizado para Backend Python
FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias de sistema para Postgres/Compilación
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Copiar dependencias
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary uvicorn

# Copiar código fuente
COPY backend/ ./backend/
COPY launcher.py .

# Variables de entorno por defecto
ENV PYTHONPATH=/app
ENV PORT=8000

# Comando de arranque
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Ajuste de Base de Datos
En `backend/app/core/database.py`, asegúrate de que se pueda leer la `DATABASE_URL` de entorno:

```python
import os
from sqlmodel import create_engine

# Render/Railway proveen esta variable
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./backend/app.db")

# Fix para SQLAlchemy < 1.4 (común en algunas nubes)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

### 3. Pasos para Railway (Opción Recomendada)
1.  Sube tu código a GitHub.
2.  En [Railway.app](https://railway.app/), crea un "New Project" desde tu repo.
3.  Añade un servicio de **PostgreSQL** al proyecto.
4.  Railway enlazará automáticamente la variable `DATABASE_URL`.
5.  Tu API estará lista en una URL pública (ej: `https://nexus-api.up.railway.app`).

---

## Parte 2: Conectar el Frontend
Para que tu App Móvil (o Web Local) se conecte a este nuevo backend en la nube, necesitas configurar la URL de la API en el frontend.

En `frontend/.env` (o `.env.production`):

```bash
PUBLIC_API_URL=https://nexus-api.up.railway.app
```
*(Asegúrate de que tu código frontend use esta variable en lugar de `localhost:8000`)*.
