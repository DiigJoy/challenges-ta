## Prompt

Necesito desarrollar una API REST en Python con FastAPI que tenga tres endpoints:

1. `/challenge/process`: debe consultar datos desde InfluxDB y procesarlos según reglas de negocio (dependiendo del valor y versión), y guardar alertas en una tabla MySQL.

2. `/challenge/search`: debe listar alertas con filtros (versión, tipo, sended) desde la base MySQL.

3. `/challenge/send`: debe actualizar alertas marcando `sended = true` según filtros.

Quiero que me ayudes a estructurar bien los modelos (SQLAlchemy), crear el flujo entre Influx y MySQL, y me recomiendes recursos para manejar este tipo de arquitectura híbrida.


---

## Respuesta de ChatGPT (resumen):

Podés construir esta arquitectura en 4 archivos separados:

1. `main.py`: donde definís los endpoints con FastAPI
2. `models.py`: modelos de SQLAlchemy para la tabla `alerts`
3. `influx_service.py`: función que consulta datos desde Influx con filtros por versión y rango de tiempo
4. `mysql_service.py`: funciones que insertan, buscan y actualizan alertas

### Flujo sugerido:

- En `/challenge/process`:
  - Recibir versión y tiempo
  - Calcular `start_time`
  - Consultar Influx filtrando por measurement y tag
  - Generar alertas según las reglas y guardarlas en MySQL

- En `/challenge/search`:
  - Armar filtros dinámicos con SQLAlchemy
  - Retornar JSON con alertas encontradas

- En `/challenge/send`:
  - Usar `update()` para marcar sended = true

### Recursos recomendados:

- [FastAPI SQLAlchemy Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Influx Python Client](https://influxdb-client.readthedocs.io/)
- [Pydantic Models](https://docs.pydantic.dev/latest/)

