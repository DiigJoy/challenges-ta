from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Alert
from dotenv import load_dotenv
import os
import time
time.sleep(10)  # Espera de 10 segundos (ajustable)

load_dotenv()

DB_USER="admin"
DB_PASSWORD="admin"
DB_HOST="mysql"
DB_PORT=3306
DB_NAME="tecnoandina"

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Función para insertar una alerta
def insert_alert(data):
    session = SessionLocal()
    alert = Alert(**data)
    session.add(alert)
    session.commit()
    session.close()

# Función para buscar alertas con filtros
def search_alerts(version=None, type=None, sended=None):
    session = SessionLocal()
    query = session.query(Alert)
    
    # Recuperando datos si es vacío
    if version is not None:
        query = query.filter(Alert.version == version)
    if type is not None:
        query = query.filter(Alert.type == type)
    if sended is not None:
        query = query.filter(Alert.sended == sended)

    results = query.all()
    session.close()
    return results

# Función para marcar como enviadas
def send_alerts(version, type_):
    session = SessionLocal()
    query = session.query(Alert).filter(
        Alert.version == version,
        Alert.type == type_,
        Alert.sended == False
    )
    updated = query.update({Alert.sended: True})
    session.commit()
    session.close()
    return updated
