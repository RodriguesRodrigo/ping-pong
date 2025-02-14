from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class StatusEnum(str, Enum):
    online = "online"
    offline = "offline"


class SiteCreate(BaseModel):
    name: str
    url: HttpUrl  # Valida se a URL é válida


class SiteResponse(BaseModel):
    site_id: int
    name: str
    url: str
    status: str

    class Config:
        from_attributes = True  # Permite conversão automática de ORM


class RequestLogCreate(BaseModel):
    site_id: int
    status_code: int
    response_time: float
    timestamp: datetime


class RequestLogResponse(BaseModel):
    request_log_id: int
    site_id: int
    status_code: int
    response_time: float
    timestamp: datetime

    class Config:
        from_attributes = True
