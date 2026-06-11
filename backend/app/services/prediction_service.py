from datetime import datetime
from datetime import timezone
from datetime import timedelta

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

from app.schemas.weather import PredictionPoint
from app.schemas.weather import PredictionResponse


def _confidence_label(score: float) -> str:
    if score >= 0.85:
        return "HIGH"
    elif score >= 0.60:
        return "MEDIUM"
    else:
        return "LOW"


class PredictionService:

    def predict(self, records, hours: int = 6) -> PredictionResponse:

        # Filtre les enregistrements sans created_at
        records = [r for r in records if r.created_at is not None]

        if not records or len(records) < 5:
            return PredictionResponse(
                station_id="unknown",
                predictions=[],
                model="PolynomialRegression(degree=2)",
                based_on_records=len(records),
                model_score=0.0,
                confidence="INSUFFICIENT_DATA",
                generated_at=datetime.now(timezone.utc),
                message="Pas assez de données (minimum 5 enregistrements valides)"
            )

        # ── Prépare les données ───────────────────────────────────────
        records_sorted = sorted(records, key=lambda r: r.created_at)

        t0 = records_sorted[0].created_at.timestamp()

        X = np.array([
            [r.created_at.timestamp() - t0]
            for r in records_sorted
        ])

        y_temp = np.array([r.temperature for r in records_sorted])
        y_hum  = np.array([r.humidity    for r in records_sorted])

        # ── Entraîne les modèles polynomiaux (degree=2) ───────────────
        model_temp = make_pipeline(
            PolynomialFeatures(degree=2),
            LinearRegression()
        )
        model_temp.fit(X, y_temp)

        model_hum = make_pipeline(
            PolynomialFeatures(degree=2),
            LinearRegression()
        )
        model_hum.fit(X, y_hum)

        # ── Calcule le R² score ───────────────────────────────────────
        score_temp = r2_score(y_temp, model_temp.predict(X))
        score_hum  = r2_score(y_hum,  model_hum.predict(X))
        avg_score  = round((score_temp + score_hum) / 2, 4)

        # ── Génère les prédictions ────────────────────────────────────
        last_ts    = records_sorted[-1].created_at
        last_x     = records_sorted[-1].created_at.timestamp() - t0
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
            model="PolynomialRegression(degree=2)",
            based_on_records=len(records),
            model_score=avg_score,
            confidence=_confidence_label(avg_score),
            generated_at=datetime.now(timezone.utc),
            message="OK"
        )