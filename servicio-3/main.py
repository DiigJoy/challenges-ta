from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service.mysql_service import insert_alert, search_alerts, send_alerts
from service.influx_service import get_data_from_influx
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import time

time.sleep(10)  # Espera de 10 segundos (ajustable)

app = FastAPI()

# Sirve la carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelos bases
class ProcessRequest(BaseModel):
    version: int
    timeSearch: str

class SearchRequest(BaseModel):
    version: int
    type: Optional[str] = None
    sended: Optional[bool] = None

class SendRequest(BaseModel):
    version: int
    type: str

# Endpoints

# Página principal (html)
@app.get("/")
def read_index():
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/challenge/process")
def process_data(req: ProcessRequest):
    try:
        data = get_data_from_influx(req.version, req.timeSearch)
        if data is None:
            raise HTTPException(status_code=422, detail="No se pudo procesar los parámetros")

        for point in data:
            value = point["value"]
            version = point["version"]

            if version == 1:
                if value > 800:
                    alert_type = "ALTA"
                elif value > 500:
                    alert_type = "MEDIA"
                elif value > 200:
                    alert_type = "BAJA"
                else:
                    continue  # no es alerta
            elif version == 2:
                if value < 200:
                    alert_type = "ALTA"
                elif value < 500:
                    alert_type = "MEDIA"
                elif value < 800:
                    alert_type = "BAJA"
                else:
                    continue  # no es alerta
            else:
                continue

            insert_alert({
                "datetime": point["datetime"],
                "value": value,
                "version": version,
                "type": alert_type,
                "sended": False
            })

        return {"status": "ok"}

    except ValueError:
        return JSONResponse(status_code=422, content={"status": "No se pudo procesar los parámetros"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": f"Error: {e}"})

@app.post("/challenge/search")
def search_data(req: SearchRequest):
    try:
        results = search_alerts(req.version, req.type, req.sended)
        formatted = []
        for r in results:
            alerta = {
                "datetime": r.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "value": r.value,
                "version": r.version,
                "type": r.type,
                "sended": r.sended
            }
            formatted.append(alerta)
        return formatted
    except ValueError:
        return JSONResponse(status_code=422, content={"status": "No se pudo procesar los parámetros"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": f"Error: {e}"})

@app.post("/challenge/send")
def send_data(req: SendRequest):
    try:
        updated = send_alerts(req.version, req.type)
        if updated > 0:
            return {"status": "ok"}
        else:
            return {"status": "ok (no alertas para enviar)"}
    except ValueError:
        return JSONResponse(status_code=422, content={"status": "No se pudo procesar los parámetros"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": f"Error: {e}"})