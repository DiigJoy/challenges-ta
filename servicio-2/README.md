# Servicio-2

Este servicio debe escuchar el tópico `challenge/dispositivo/rx` del servicio mqtt(mosquitto).
Cada mensaje que llegue se debe insertar en el servicio influx, teniendo en consideración que el **time** y **value** son *fields* y **version** es un *tag*.
Este mensaje se guardará en el bucket **system** en el measurement **dispositivos**.

---

# Servicio-2 – Suscriptor MQTT con escritura en InfluxDB

Este servicio escucha mensajes MQTT del tópico `challenge/dispositivo/rx` publicado por el **servicio-1**, y los guarda en **InfluxDB** como series temporales.

---

Fue aplicado un archivo .env para manejar credenciales sensibles (como tokens de InfluxDB o conexión a MySQL). 

---
## ¿Qué hace este servicio?
- Se suscribe al tópico MQTT `challenge/dispositivo/rx`
- Por cada mensaje recibido:
  - Lo decodifica desde JSON
  - Inserta un punto en InfluxDB con:
    - `time` y `value` como **fields**
    - `version` como **tag**
- Guarda los datos en:
  - **Bucket**: `system`
  - **Measurement**: `dispositivos`

---

## Tecnologías utilizadas
- Python
- MQTT (paho-mqtt)
- InfluxDB v2
- Librería `influxdb-client`

---

## Recursos utilizados
- [Paho MQTT Python Client Docs](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)
- [InfluxDB Python Client](https://influxdb-client.readthedocs.io/en/latest/)
- [Influx Line Protocol & Tags](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/line-protocol/)

---

## Apoyo de Inteligencia Artificial (ChatGPT)
-Lo puede acceder en el archivo uso_IA.md

---


## Cómo ejecutar este servicio

1. Asegurarse de que:
   - Mosquitto está activo
   - InfluxDB está corriendo y configurado con bucket `system`
   - El token y URL están bien configurados en el script

2. Ejecutar el script:

```bash
python servicio_2.py
```

---



## Screenshoot
![recibir_mensajes_mosquitto](images/image.png)

- Ejemplo de como recibir mensajes con mosquitto
https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html

![conexion_influxDB](images/image-1.png)

- Ejemplo de como establecer conexión con InfluxDB
https://influxdb-client.readthedocs.io/en/latest/usage.html