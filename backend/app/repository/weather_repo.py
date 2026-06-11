from datetime import datetime
from datetime import timezone
from datetime import timedelta

from sqlalchemy import func
from sqlalchemy import cast
from sqlalchemy import Date
from sqlalchemy import Numeric
from sqlalchemy import distinct

from app.models.weather import Weather


class WeatherRepository:

    @staticmethod
    def create(db, data):
        weather = Weather(
            station_id=data.station_id,
            temperature=data.temperature,
            humidity=data.humidity,
            light_raw=data.light_raw,
            light_percent=data.light_percent,
            heat_index=data.heat_index,
            dew_point=data.dew_point,
            latitude=data.latitude,
            longitude=data.longitude
        )
        db.add(weather)
        db.commit()
        db.refresh(weather)
        return weather

    @staticmethod
    def get_stations(db):
        return db.query(
            distinct(Weather.station_id).label("station_id"),
            Weather.latitude,
            Weather.longitude,
            func.max(Weather.created_at).label("last_seen"),
            func.count(Weather.id).label("record_count"),
        ).group_by(
            Weather.station_id,
            Weather.latitude,
            Weather.longitude
        ).all()

    @staticmethod
    def get_latest(db, station_id: str = None):
        query = db.query(Weather).order_by(Weather.created_at.desc())
        if station_id:
            query = query.filter(Weather.station_id == station_id)
        return query.first()

    @staticmethod
    def get_last_records(db, limit=100, station_id: str = None):
        query = db.query(Weather).order_by(Weather.created_at.desc())
        if station_id:
            query = query.filter(Weather.station_id == station_id)
        return query.limit(limit).all()

    @staticmethod
    def get_summary(db, station_id: str = None):
        query = db.query(
            func.count(Weather.id).label("total_records"),
            func.min(Weather.temperature).label("temp_min"),
            func.max(Weather.temperature).label("temp_max"),
            func.round(func.avg(Weather.temperature).cast(Numeric), 2).label("temp_avg"),
            func.min(Weather.humidity).label("humidity_min"),
            func.max(Weather.humidity).label("humidity_max"),
            func.round(func.avg(Weather.humidity).cast(Numeric), 2).label("humidity_avg"),
            func.min(Weather.light_percent).label("light_min"),
            func.max(Weather.light_percent).label("light_max"),
            func.round(func.avg(Weather.light_percent).cast(Numeric), 2).label("light_avg"),
            func.round(func.avg(Weather.heat_index).cast(Numeric), 2).label("heat_index_avg"),
            func.round(func.avg(Weather.dew_point).cast(Numeric), 2).label("dew_point_avg"),
        )
        if station_id:
            query = query.filter(Weather.station_id == station_id)
        return query.first()

    @staticmethod
    def get_daily_stats(db, days: int = 7):
        since = datetime.now(timezone.utc) - timedelta(days=days)
        return db.query(
            cast(Weather.created_at, Date).label("day"),
            func.min(Weather.temperature).label("temp_min"),
            func.max(Weather.temperature).label("temp_max"),
            func.round(func.avg(Weather.temperature).cast(Numeric), 2).label("temp_avg"),
            func.min(Weather.humidity).label("humidity_min"),
            func.max(Weather.humidity).label("humidity_max"),
            func.round(func.avg(Weather.humidity).cast(Numeric), 2).label("humidity_avg"),
            func.round(func.avg(Weather.light_percent).cast(Numeric), 2).label("light_avg"),
            func.count(Weather.id).label("record_count"),
        ).filter(
            Weather.created_at >= since
        ).group_by(
            cast(Weather.created_at, Date)
        ).order_by(
            cast(Weather.created_at, Date).desc()
        ).all()

    @staticmethod
    def get_hourly_stats(db, hours: int = 24):
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        return db.query(
            func.date_trunc("hour", Weather.created_at).label("hour"),
            func.round(func.avg(Weather.temperature).cast(Numeric), 2).label("temp_avg"),
            func.round(func.avg(Weather.humidity).cast(Numeric), 2).label("humidity_avg"),
            func.round(func.avg(Weather.light_percent).cast(Numeric), 2).label("light_avg"),
            func.count(Weather.id).label("record_count"),
        ).filter(
            Weather.created_at >= since
        ).group_by(
            func.date_trunc("hour", Weather.created_at)
        ).order_by(
            func.date_trunc("hour", Weather.created_at).desc()
        ).all()