from app.repository.weather_repo import WeatherRepository


class WeatherService:

    def __init__(self):
        self.repo = WeatherRepository()

    def save_weather(self, db, data):
        return self.repo.create(db, data)

    def latest_weather(self, db):
        return self.repo.get_latest(db)

    def history(self, db, limit=100):
        return self.repo.get_last_records(db, limit)

    def get_summary(self, db):
        return self.repo.get_summary(db)

    def get_daily_stats(self, db, days: int = 7):
        return self.repo.get_daily_stats(db, days)

    def get_hourly_stats(self, db, hours: int = 24):
        return self.repo.get_hourly_stats(db, hours)