from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Alert(Base):
    __tablename__ = 'alerts'

    id_alerta = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    version = Column(Integer, nullable=False)
    type = Column(Enum('BAJA', 'MEDIA', 'ALTA'), nullable=False)
    sended = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
