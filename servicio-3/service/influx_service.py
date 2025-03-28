from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta, timezone


# Configuración InfluxDB
INFLUX_URL = "http://influx:8086"
INFLUX_TOKEN = "Qo5ujokcLZKV2q2YhWFWU7XcpD_0dlv0n8w2bIeJ4BcUvzynCPBGGaA_8xeiK5T5KUgApbMUJUHh5o45JtSIjw=="
INFLUX_ORG = "tecnoandina"
INFLUX_BUCKET = "system"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# Genera el datetime a partir de la string inserida
def get_start_time(time_search: str):
    print(f"[DEBUG] time_search recibido: '{time_search}'")
    if not time_search or len(time_search) < 2:
        raise ValueError("Formato inválido. Ejemplo: '15m', '3h', '2d'")

    cantidad = time_search[:-1]
    unidad = time_search[-1]

    if not cantidad.isdigit():
        raise ValueError("La cantidad debe ser numérica")

    cantidad = int(cantidad)

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
                try:
                    version_val = record.values.get("version")
                    value_val = record.get_value()

                    if not version_val or not str(version_val).isdigit():
                        print(f"[WARN] Valor de 'version' inválido: {version_val}")
                        continue

                    if value_val is None or value_val == '':
                        print(f"[WARN] Valor de 'value' vacío: {value_val}")
                        continue

                    data_points.append({
                        "datetime": record.get_time(),
                        "value": float(value_val),
                        "version": int(version_val)
                    })

                except Exception as e:
                    print(f"[ERROR] Registro descartado por excepción: {e}")
                    continue
    except Exception as e:
        print(f"[ERROR Influx] {e}")
        return None
