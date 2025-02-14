from sqlalchemy import desc
from sqlalchemy.orm import Session

from src import schemas
from src.models import RequestLog, Site


def is_url_exists(db: Session, url: str) -> bool:
    return db.query(db.query(Site).filter(Site.url == url).exists()).scalar()


def create_site(db: Session, site: schemas.SiteCreate) -> schemas.SiteResponse:
    if is_url_exists(db, str(site.url)):
        raise ValueError(f"url {site.url} already exist")

    db_site = Site(name=site.name, url=str(site.url))
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return schemas.SiteResponse.from_orm(db_site)


def get_all_sites(db: Session) -> list[schemas.SiteResponse | None]:
    return [schemas.SiteResponse.from_orm(site) for site in db.query(Site).all()]


def update_site_status(db: Session, site_id: int, new_status: schemas.StatusEnum) -> None:
    db_site = db.query(Site).filter(Site.site_id == site_id).first()
    if not db_site:
        print(f"update_status_site warning: site {site_id} not found")
        return

    db_site.status = new_status.value
    db.commit()


def create_request_log(db: Session, request_log: schemas.RequestLogCreate) -> schemas.RequestLogResponse:
    db_request_log = RequestLog(**request_log.model_dump())
    db.add(db_request_log)
    db.commit()
    db.refresh(db_request_log)
    return schemas.RequestLogResponse.from_orm(db_request_log)


def get_request_log_from_site_id(db: Session, site_id: int) -> list[schemas.RequestLogResponse | None]:
    db_request_log = db.query(RequestLog).filter(
        RequestLog.site_id == site_id
    ).order_by(desc(RequestLog.timestamp)).all()
    return [schemas.RequestLogResponse.from_orm(request_log) for request_log in db_request_log]
