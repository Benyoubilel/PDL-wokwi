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