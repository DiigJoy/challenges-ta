# Dockerfile con la imagen y pasos para dejar funcionando el servicio
# puede ser igual al del servicio-1 y servicio-2
FROM python:3.10-slim

WORKDIR /app

COPY . .

# Copia el script wait-for-it desde la raíz del proyecto
COPY ../scripts/wait-for-it.sh ./wait-for-it.sh
RUN chmod +x ./wait-for-it.sh

RUN pip install --no-cache-dir -r requirements.txt

# Usa wait-for-it para esperar MySQL antes de lanzar FastAPI
CMD ["./wait-for-it.sh", "mysql", "3306", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
