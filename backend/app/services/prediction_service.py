from datetime import datetime
from datetime import timezone
from datetime import timedelta

import numpy as np
from sklearn.linear_model import LinearRegression  # ✅

from app.schemas.weather import PredictionPoint
from app.schemas.weather import PredictionResponse


class PredictionService:

    def predict(self, records, hours: int = 6) -> PredictionResponse:

        records = [r for r in records if r.created_at is not None]
        if not records or len(records) < 3:
            return PredictionResponse(
                station_id="unknown",
                predictions=[],
                model="LinearRegression",
                based_on_records=0,
                generated_at=datetime.now(timezone.utc),
                message="Pas assez de données pour prédire (minimum 3 enregistrements)"
            )

        # ── Prépare les données ───────────────────────────────────────
        records_sorted = sorted(records, key=lambda r: r.created_at)

        # Convertit les timestamps en secondes depuis le premier enregistrement
        t0 = records_sorted[0].created_at.timestamp()
        X = np.array([
            [r.created_at.timestamp() - t0]
            for r in records_sorted
        ])

        y_temp = np.array([r.temperature for r in records_sorted])
        y_hum  = np.array([r.humidity    for r in records_sorted])

        # ── Entraîne les modèles ──────────────────────────────────────
        model_temp = LinearRegression()
        model_temp.fit(X, y_temp)

        model_hum = LinearRegression()
        model_hum.fit(X, y_hum)

        # ── Génère les prédictions ────────────────────────────────────
        last_ts   = records_sorted[-1].created_at
        last_x    = records_sorted[-1].created_at.timestamp() - t0
        station_id = records_sorted[-1].station_id

        predictions = []

        for h in range(1, hours + 1):

            future_ts = last_ts + timedelta(hours=h)
            future_x  = np.array([[last_x + h * 3600]])

            temp_pred = round(float(model_temp.predict(future_x)[0]), 2)
            hum_pred  = round(float(model_hum.predict(future_x)[0]),  2)

            # Clamp dans des bornes physiques réalistes
            temp_pred = max(-50.0, min(70.0,  temp_pred))
            hum_pred  = max(  0.0, min(100.0, hum_pred))

            predictions.append(PredictionPoint(
                hour=future_ts,
                temperature=temp_pred,
                humidity=hum_pred
            ))

        return PredictionResponse(
            station_id=station_id,
            predictions=predictions,
            model="LinearRegression",
            based_on_records=len(records),
            generated_at=datetime.now(timezone.utc),
            message="OK"
        )