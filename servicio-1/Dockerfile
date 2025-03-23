# Dockerfile con la imagen y pasos para dejar funcionando el servicio
# puede ser igual al del servicio-2 y servicio-3
# Imagen base
FROM python:3.10-slim

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos
COPY servicio_1.py . 
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el script
CMD ["python", "servicio_1.py"]
