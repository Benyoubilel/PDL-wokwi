from app.repository.weather_repo import WeatherRepository


class WeatherService:

    def __init__(self):
        self.repo = WeatherRepository()

    def save_weather(self, db, data):
        return self.repo.create(db, data)

    def latest_weather(self, db, station_id: str = None):
        return self.repo.get_latest(db, station_id)

    def history(self, db, limit=100, station_id: str = None):
        return self.repo.get_last_records(db, limit, station_id)

    def get_stations(self, db):
        return self.repo.get_stations(db)

    def get_summary(self, db, station_id: str = None):
        row = self.repo.get_summary(db, station_id)
        if row is None:
            return None
        return {
            "total_records": row.total_records,
            "temp_min":       row.temp_min,
            "temp_max":       row.temp_max,
            "temp_avg":       float(row.temp_avg),
            "humidity_min":   row.humidity_min,
            "humidity_max":   row.humidity_max,
            "humidity_avg":   float(row.humidity_avg),
            "light_min":      row.light_min,
            "light_max":      row.light_max,
            "light_avg":      float(row.light_avg),
            "heat_index_avg": float(row.heat_index_avg),
            "dew_point_avg":  float(row.dew_point_avg),
        }

    def get_daily_stats(self, db, days: int = 7):
        return self.repo.get_daily_stats(db, days)

    def get_hourly_stats(self, db, hours: int = 24):
        return self.repo.get_hourly_stats(db, hours)