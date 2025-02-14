from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database import Base


class Site(Base):
    __tablename__ = "sites"

    site_id = Column(Integer, name="id", primary_key=True, index=True)
    name = Column(String, nullable=False)  # Nome do site definido pelo usuário
    url = Column(String, unique=True, nullable=False)  # URL do site
    status = Column(String, default="desconhecido")  # Status atual do site
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação do site

    logs = relationship("RequestLog", back_populates="site")  # Relacionamento


class RequestLog(Base):
    __tablename__ = "request_logs"

    request_log_id = Column(Integer, name="id", primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    status_code = Column(Integer)  # Status code da requisição (ex: 200, 404)
    response_time = Column(Float)  # Tempo de resposta em segundos
    timestamp = Column(DateTime)  # Horário da requisição

    site = relationship("Site", back_populates="logs")
