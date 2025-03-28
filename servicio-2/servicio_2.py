import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from datetime import datetime



# Configuración MQTT
BROKER = "mosquitto"
PORT = 1883
TOPIC = "challenge/dispositivo/rx"

# Configuración InfluxDB
INFLUX_URL = "http://influx:8086"
INFLUX_TOKEN = "AildXuWB88Ue-APuLafSJOi2ORLjtoI6utX6hBMtt8FDxNp5rA70wGIiH600h1NhWCuY6iRXCSlTM0yU_ViABA=="
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

        # 🔥 Este timestamp debe ir aquí, no arriba del archivo
        timestamp = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S").isoformat() + "Z"

        point = (
            Point("dispositivos")
            .tag("version", str(data["version"]))
            .field("value", float(data["value"]))
            .time(timestamp) # Usa el campo time como timestamp real

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
