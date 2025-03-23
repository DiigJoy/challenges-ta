## Prompt

-Necesito desarrollar un servicio en Python que escuche un tópico MQTT (con Mosquitto) y, cada vez que reciba un mensaje en formato JSON, lo guarde en InfluxDB. El mensaje tiene las claves `time`, `value` y `version`.

`time` y `value` deben ser guardados como **fields**, y `version` como un **tag**. El bucket es `system` y el measurement `dispositivos`.

Quiero que me ayudes a estructurar el servicio, incluyendo la conexión MQTT, el uso de callbacks para recibir los mensajes y la escritura en InfluxDB v2 usando su cliente oficial. Además, si puedes, recomiéndame documentación para seguir aprendiendo.

---

## Response:

¡Claro! Podés usar las librerías `paho-mqtt` para suscribirte a un tópico, y `influxdb-client` para insertar los puntos en InfluxDB 2.

### 🔄 Flujo del servicio:

1. Conectarse al broker MQTT
2. Suscribirse al tópico deseado
3. Implementar la función `on_message(client, userdata, msg)`
4. Parsear el `msg.payload` como JSON
5. Construir un `Point` de Influx con:
   - `Point("dispositivos")`
   - `.tag("version", str(data["version"]))`
   - `.field("value", float(data["value"]))`
   - `.field("time", data["time"])` (solo para visualización)

6. Usar `write_api.write(...)` para guardar el dato

### 🔧 Recomendaciones:

- Asegurate de tener InfluxDB accesible en `http://localhost:8086`
- Tené a mano tu **token**, **org** y **bucket**
- El `loop_forever()` de MQTT asegura que el cliente se quede escuchando
- Influx insertará automáticamente un timestamp si no se indica uno

### 📘 Documentación sugerida:

- [InfluxDB Python Client Docs](https://influxdb-client.readthedocs.io/en/latest/)
- [Line Protocol & Best Practices](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/line-protocol/)
- [Paho MQTT Docs](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)
