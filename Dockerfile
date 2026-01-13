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