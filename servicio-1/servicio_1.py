import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

# Configuración mosquitto
BROKER = "localhost" 
PORT = 1883
TOPIC = "challenge/dispositivo/rx"

# Callback para conexión exitosa https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[INFO] Conectado al broker MQTT con código: {reason_code}")

# Inicializar cliente
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# Conectar al broker
client.connect(BROKER, PORT, 60)
client.loop_start()  # Use loop_start en lugar de loop_forever para poder continuar con el flujo del programa

# Publicar un mensaje cada 60 segundos
while True:
    payload = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": round(random.uniform(0, 1000), 2),
        "version": random.choice([1, 2])
    }

    # Convertir a JSON y publicar
    client.publish(TOPIC, json.dumps(payload))
    print(f"[INFO] Publicado: {payload}")
    
    time.sleep(60)