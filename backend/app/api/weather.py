from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.weather import AlertsResponse
from app.services.alert_service import AlertService
from app.schemas.weather import WeatherCreate
from app.schemas.weather import WeatherResponse
from app.schemas.weather import StatsSummary
from app.schemas.weather import DailyStats
from app.schemas.weather import HourlyStats
from app.schemas.weather import PredictionResponse
from app.services.prediction_service import PredictionService
from app.services.weather_service import WeatherService


router = APIRouter(
    tags=["Weather"]
)

service = WeatherService()
alert_service = AlertService()
prediction_service = PredictionService()

@router.get("/health")
def health():
    return {
        "status": "UP"
    }


@router.post("/weather", response_model=WeatherResponse)
def create_weather(
    data: WeatherCreate,
    db: Session = Depends(get_db)
):
    return service.save_weather(db, data)


@router.get("/weather/latest", response_model=WeatherResponse)
def latest_weather(
    db: Session = Depends(get_db)
):
    return service.latest_weather(db)


@router.get("/weather", response_model=List[WeatherResponse])
def get_weather(
    db: Session = Depends(get_db)
):
    return service.history(db)


@router.get("/weather/stats/summary", response_model=StatsSummary)
def get_summary(
    db: Session = Depends(get_db)
):
    return service.get_summary(db)


@router.get("/weather/stats/daily", response_model=List[DailyStats])
def get_daily_stats(
    days: int = 7,
    db: Session = Depends(get_db)
):
    return service.get_daily_stats(db, days)


@router.get("/weather/stats/hourly", response_model=List[HourlyStats])
def get_hourly_stats(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    return service.get_hourly_stats(db, hours)


@router.get("/weather/alerts", response_model=AlertsResponse)
def get_alerts(
    db: Session = Depends(get_db)
):
    latest = service.latest_weather(db)
    return alert_service.check_alerts(latest)

@router.get("/weather/predict", response_model=PredictionResponse)
def get_prediction(
    hours: int = 6,
    db: Session = Depends(get_db)
):
    records = service.history(db, limit=100)
    return prediction_service.predict(records, hours)