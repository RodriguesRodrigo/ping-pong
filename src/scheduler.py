import os
import time

from datetime import datetime

import requests
import schedule

from fastapi import status
from sqlalchemy.orm import Session

from src import services
from src.database import SessionLocal
from src.schemas import RequestLogCreate, StatusEnum


def read_status():
    status_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".scheduler_status")

    if os.path.exists(status_file):
        with open(status_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "stopped"  # Se o arquivo não existir ou estiver vazio, assume que o status é "stopped"


def site_request(url: str) -> None:
    try:
        response = requests.get(url, timeout=10)
        print(f"{response.status_code} - {url} - {response.elapsed.total_seconds()}s")

        return {
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "timestamp": datetime.now(),
        }
    except Exception as error:
        print(f"site_request error: {error}")
        return {
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "response_time": 0,
            "timestamp": datetime.now(),
        }


def save_response(db: Session, site_id: int, status_code: int, response_time: float, timestamp: datetime) -> None:
    request_log = RequestLogCreate(
        site_id=site_id,
        status_code=status_code,
        response_time=response_time,
        timestamp=timestamp,
    )
    try:
        services.create_request_log(db, request_log)
    except Exception as error:
        print(f"save_response error: {error}")


def handle_site_monitoring() -> None:
    db = SessionLocal()
    for site in services.get_all_sites(db):
        response = site_request(site.url)
        save_response(**response, db=db, site_id=site.site_id)

        status_response = StatusEnum.online if response["status_code"] == 200 else StatusEnum.offline
        if site.status != status_response:
            services.update_site_status(db, site.site_id, status_response)


def run() -> None:
    delay = 10
    schedule.every(delay).seconds.do(handle_site_monitoring).tag("site-monitoring")
    while True:
        scheduler_status = read_status()
        if scheduler_status == "running":
            schedule.run_all(delay_seconds=delay)
        else:
            print("Scheduler está parado.")
            time.sleep(delay)
