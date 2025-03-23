## Prompt:
-Necesito desarrollar un servicio de mensajeria con mosquitto y python, en el cual se enviara un mensaje en formato json, el json tendrá time, un valor flotante entre 0 y 1000 con 2 decimales, y version que sera 1 o 2. Necesito que me ayudes a estructurar el servicio, ademas de darme herramientas como documentación u otro dato para reenforzar el aprendizado y donde referirme a futuro en caso de modificaciones.


---

## Response:
-¡Claro! Para desarrollar ese servicio de mensajería en Python usando Mosquitto (MQTT), podés usar la librería paho-mqtt, que es una de las más populares y bien documentadas.

###  Flujo del servicio:
-📦 Estructura básica del servicio
-Este servicio actuará como publisher (publicador MQTT), enviando un JSON cada cierto intervalo al broker Mosquitto.

import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC = "tu_topico"

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[INFO] Conectado al broker MQTT con código: {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

while True:
    payload = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": round(random.uniform(0, 1000), 2),
        "version": random.choice([1, 2])
    }
    client.publish(TOPIC, json.dumps(payload))
    print(f"[INFO] Publicado: {payload}")
    time.sleep(60)

## 🧠 Recomendaciones:
Asegurate de tener Mosquitto corriendo en localhost:1883

Este script publica cada 60 segundos (podés ajustar el sleep)

El tópico puede ser cualquier string jerárquico, ej: sala/sensor/temp

## 📘 Recursos de aprendizaje:
Paho MQTT Python Client Docs
-https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html

MQTT Essentials - HiveMQ
-https://www.hivemq.com/mqtt/

Mosquitto Docs
-https://mosquitto.org/documentation/

Este servicio es ideal para simular dispositivos en entornos IoT, sensores o sistemas distribuidos de monitoreo.