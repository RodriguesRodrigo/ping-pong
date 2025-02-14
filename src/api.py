from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import schemas
from src import services
from src.database import get_db


router = APIRouter()


@router.get("/health/")
def get_health() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok"})


@router.post("/site/", response_model=schemas.SiteCreate)
def create_site(site: schemas.SiteCreate, db: Session = Depends(get_db)) -> JSONResponse:
    try:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(services.create_site(db, site)),
        )
    except Exception as error:
        print(error)  # TODO: configurar logging
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(error)})


@router.get("/site/", response_model=schemas.SiteResponse)
def get_all_sites(db: Session = Depends(get_db)) -> JSONResponse:
    # TODO: filtrar sites por usuário logado!
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(services.get_all_sites(db)))


@router.get("/logs/{site_id}")
def get_request_log_from_site_id(site_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(services.get_request_log_from_site_id(db, site_id)),
    )
