# Dockerfile con la imagen y pasos para dejar funcionando el servicio
# puede ser igual al del servicio-1 y servicio-2
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]