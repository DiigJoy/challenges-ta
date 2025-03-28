from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta, timezone


# Configuración InfluxDB
INFLUX_URL = "http://influx:8086"
INFLUX_TOKEN = "AildXuWB88Ue-APuLafSJOi2ORLjtoI6utX6hBMtt8FDxNp5rA70wGIiH600h1NhWCuY6iRXCSlTM0yU_ViABA=="
INFLUX_ORG = "tecnoandina"
INFLUX_BUCKET = "system"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# Genera el datetime a partir de la string inserida
def get_start_time(time_search: str):
    """
    Convierte un string como '15m', '2h', '3d' en un datetime
    """
    cantidad = int(time_search[:-1]) # Accede a la string menos el último valor (m, h o d)
    unidad = time_search[-1] # Accede al último valor de la string para hacer la conversión correcta.

    if unidad == 'm':
        delta = timedelta(minutes=cantidad)
    elif unidad == 'h':
        delta = timedelta(hours=cantidad)
    elif unidad == 'd':
        delta = timedelta(days=cantidad)
    else:
        raise ValueError("Unidad inválida. Usa 'm', 'h' o 'd'.")

    return datetime.now(timezone.utc) - delta

def get_data_from_influx(version: int, time_search: str):
    try:
        start_time = get_start_time(time_search).isoformat()

        query = f'''
        from(bucket: "{INFLUX_BUCKET}")
          |> range(start: {start_time})
          |> filter(fn: (r) => r["_measurement"] == "dispositivos")
          |> filter(fn: (r) => r["version"] == "{version}")
          |> filter(fn: (r) => r["_field"] == "value")
        '''

        result = query_api.query(org=INFLUX_ORG, query=query)

        data_points = []
        for table in result:
            for record in table.records:
                data_points.append({
                    "datetime": record.get_time(),
                    "value": record.get_value(),
                    "version": int(record.values["version"])
                })

        return data_points

    except Exception as e:
        print(f"[ERROR Influx] {e}")
        return None
