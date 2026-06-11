from datetime import datetime
from datetime import timezone

from app.schemas.weather import WeatherAlert
from app.schemas.weather import AlertsResponse


THRESHOLDS = {
    "temp_high_warning":      35.0,
    "temp_high_critical":     40.0,
    "temp_low_warning":        5.0,
    "temp_low_critical":       0.0,

    "humidity_high_warning":  85.0,
    "humidity_high_critical": 95.0,
    "humidity_low_warning":   20.0,
    "humidity_low_critical":  10.0,

    "heat_index_warning":     38.0,
    "heat_index_critical":    45.0,

    "light_high_warning":     90.0,
}


class AlertService:

    def check_alerts(self, reading) -> AlertsResponse:

        if reading is None:
            return AlertsResponse(
                status="NO_DATA",
                alerts=[],
                checked_at=datetime.now(timezone.utc),
                station_id="unknown"
            )

        alerts = []

        # ── Température ──────────────────────────────────────────────
        if reading.temperature >= THRESHOLDS["temp_high_critical"]:
            alerts.append(WeatherAlert(
                type="HIGH_TEMPERATURE",
                message=f"Température critique : {reading.temperature}°C",
                value=reading.temperature,
                threshold=THRESHOLDS["temp_high_critical"],
                severity="CRITICAL"
            ))
        elif reading.temperature >= THRESHOLDS["temp_high_warning"]:
            alerts.append(WeatherAlert(
                type="HIGH_TEMPERATURE",
                message=f"Température élevée : {reading.temperature}°C",
                value=reading.temperature,
                threshold=THRESHOLDS["temp_high_warning"],
                severity="WARNING"
            ))

        if reading.temperature <= THRESHOLDS["temp_low_critical"]:
            alerts.append(WeatherAlert(
                type="LOW_TEMPERATURE",
                message=f"Température critique basse : {reading.temperature}°C",
                value=reading.temperature,
                threshold=THRESHOLDS["temp_low_critical"],
                severity="CRITICAL"
            ))
        elif reading.temperature <= THRESHOLDS["temp_low_warning"]:
            alerts.append(WeatherAlert(
                type="LOW_TEMPERATURE",
                message=f"Température basse : {reading.temperature}°C",
                value=reading.temperature,
                threshold=THRESHOLDS["temp_low_warning"],
                severity="WARNING"
            ))

        # ── Humidité ─────────────────────────────────────────────────
        if reading.humidity >= THRESHOLDS["humidity_high_critical"]:
            alerts.append(WeatherAlert(
                type="HIGH_HUMIDITY",
                message=f"Humidité critique : {reading.humidity}%",
                value=reading.humidity,
                threshold=THRESHOLDS["humidity_high_critical"],
                severity="CRITICAL"
            ))
        elif reading.humidity >= THRESHOLDS["humidity_high_warning"]:
            alerts.append(WeatherAlert(
                type="HIGH_HUMIDITY",
                message=f"Humidité élevée : {reading.humidity}%",
                value=reading.humidity,
                threshold=THRESHOLDS["humidity_high_warning"],
                severity="WARNING"
            ))

        if reading.humidity <= THRESHOLDS["humidity_low_critical"]:
            alerts.append(WeatherAlert(
                type="LOW_HUMIDITY",
                message=f"Humidité critique basse : {reading.humidity}%",
                value=reading.humidity,
                threshold=THRESHOLDS["humidity_low_critical"],
                severity="CRITICAL"
            ))
        elif reading.humidity <= THRESHOLDS["humidity_low_warning"]:
            alerts.append(WeatherAlert(
                type="LOW_HUMIDITY",
                message=f"Humidité basse : {reading.humidity}%",
                value=reading.humidity,
                threshold=THRESHOLDS["humidity_low_warning"],
                severity="WARNING"
            ))

        # ── Heat Index ───────────────────────────────────────────────
        if reading.heat_index >= THRESHOLDS["heat_index_critical"]:
            alerts.append(WeatherAlert(
                type="DANGEROUS_HEAT_INDEX",
                message=f"Heat index dangereux : {reading.heat_index}°C",
                value=reading.heat_index,
                threshold=THRESHOLDS["heat_index_critical"],
                severity="CRITICAL"
            ))
        elif reading.heat_index >= THRESHOLDS["heat_index_warning"]:
            alerts.append(WeatherAlert(
                type="HIGH_HEAT_INDEX",
                message=f"Heat index élevé : {reading.heat_index}°C",
                value=reading.heat_index,
                threshold=THRESHOLDS["heat_index_warning"],
                severity="WARNING"
            ))

        # ── Luminosité ───────────────────────────────────────────────
        if reading.light_percent >= THRESHOLDS["light_high_warning"]:
            alerts.append(WeatherAlert(
                type="HIGH_LIGHT",
                message=f"Luminosité très forte : {reading.light_percent}%",
                value=reading.light_percent,
                threshold=THRESHOLDS["light_high_warning"],
                severity="WARNING"
            ))

        return AlertsResponse(
            status="ALERT" if alerts else "OK",
            alerts=alerts,
            checked_at=datetime.now(timezone.utc),
            station_id=reading.station_id
        )