from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.weather import WeatherCreate
from app.services.weather_service import WeatherService

router = APIRouter(
    tags=["Weather"]
)

service = WeatherService()


@router.get("/health")
def health():
    return {
        "status": "UP"
    }


@router.post("/weather")
def create_weather(
    data: WeatherCreate,
    db: Session = Depends(get_db)
):
    return service.save_weather(db, data)


@router.get("/weather/latest")
def latest_weather(
    db: Session = Depends(get_db)
):
    return service.latest_weather(db)


@router.get("/weather")
def get_weather(
    db: Session = Depends(get_db)
):
    return service.history(db)