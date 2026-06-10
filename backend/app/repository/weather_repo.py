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
            dew_point=data.dew_point
        )

        db.add(weather)
        db.commit()
        db.refresh(weather)

        return weather

    @staticmethod
    def get_latest(db):

        return (
            db.query(Weather)
            .order_by(Weather.created_at.desc())
            .first()
        )

    @staticmethod
    def get_last_records(db, limit=100):

        return (
            db.query(Weather)
            .order_by(Weather.created_at.desc())
            .limit(limit)
            .all()
        )