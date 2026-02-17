# Backend Dockerfile para Cloud Run
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Puerto
EXPOSE 8080

# Comando para ejecutar
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 120 wiki_api.wsgi:application




