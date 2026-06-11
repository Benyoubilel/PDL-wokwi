from typing import List
from datetime import datetime
from datetime import timezone
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
from app.schemas.weather import DashboardResponse
from app.schemas.weather import StationInfo 
from typing import List
from typing import Optional

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


@router.get("/weather/stations", response_model=List[StationInfo])
def get_stations(
    db: Session = Depends(get_db)
):
    return service.get_stations(db)


@router.get("/weather/latest", response_model=WeatherResponse)
def latest_weather(
    station_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return service.latest_weather(db, station_id)



@router.get("/weather", response_model=List[WeatherResponse])
def get_weather(
    station_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return service.history(db, limit=100, station_id=station_id)


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
    station_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    latest = service.latest_weather(db, station_id)
    return alert_service.check_alerts(latest)

@router.get("/weather/predict", response_model=PredictionResponse)
def get_prediction(
    hours: int = 6,
    station_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    records = service.history(db, limit=100, station_id=station_id)
    return prediction_service.predict(records, hours)


@router.get("/weather/dashboard", response_model=DashboardResponse)
def get_dashboard(
    station_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    latest      = service.latest_weather(db, station_id)
    summary     = service.get_summary(db, station_id)
    alerts      = alert_service.check_alerts(latest)
    predictions = prediction_service.predict(
        service.history(db, limit=100, station_id=station_id)
    )

    return DashboardResponse(
        station_id=latest.station_id if latest else "unknown",
        latitude=latest.latitude   if latest else None,
        longitude=latest.longitude if latest else None,
        generated_at=datetime.now(timezone.utc),
        latest=latest,
        summary=summary,
        alerts=alerts,
        predictions=predictions
    )