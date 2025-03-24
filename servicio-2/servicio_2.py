import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración MQTT
BROKER = "mosquitto"
PORT = 1883
TOPIC = "challenge/dispositivo/rx"

# Configuración InfluxDB
INFLUX_URL = "http://influx:8086"
INFLUX_TOKEN = "_Gcd7AQSMFyOpbINETVW1DPW7Zi0rQCsX2SMwfX7BctoHJ7der7cm4H1VNAORWN0c4DdkpIPFQJk_ntqvxqsPw=="
INFLUX_ORG = "tecnoandina"
INFLUX_BUCKET = "system"


# Inicializar InfluxDB client
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api()

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"[INFO] Mensaje recibido: {data}")

        point = (
            Point("dispositivos")
            .tag("version", str(data["version"]))
            .field("time", data["time"])  # string, solo para visualizar
            .field("value", float(data["value"]))
        )

        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("[INFO] Insertado en InfluxDB")

    except Exception as e:
        print(f"[ERROR] {e}")


# Conectar MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print(f"[INFO] Escuchando tópico: {TOPIC}")
client.loop_forever()
