from pydantic import BaseModel
from pydantic import Field
from datetime import datetime
from datetime import date
from typing import Optional
from typing import List
from typing import Optional

class WeatherCreate(BaseModel):
    station_id: str

    temperature: float = Field(
        ge=-50,
        le=70
    )

    humidity: float = Field(
        ge=0,
        le=100
    )

    light_raw: float

    light_percent: float = Field(
        ge=0,
        le=100
    )

    heat_index: float

    dew_point: float


class WeatherResponse(BaseModel):
    id: int

    station_id: str

    temperature: float

    humidity: float

    light_raw: float

    light_percent: float

    heat_index: float

    dew_point: float

    created_at: Optional[datetime] = None 

    model_config = {
        "from_attributes": True
    }


class StatsSummary(BaseModel):
    total_records: int

    temp_min: float
    temp_max: float
    temp_avg: float

    humidity_min: float
    humidity_max: float
    humidity_avg: float

    light_min: float
    light_max: float
    light_avg: float

    heat_index_avg: float
    dew_point_avg: float


class DailyStats(BaseModel):
    day: date

    temp_min: float
    temp_max: float
    temp_avg: float

    humidity_min: float
    humidity_max: float
    humidity_avg: float

    light_avg: float

    record_count: int


class HourlyStats(BaseModel):
    hour: datetime

    temp_avg: float
    humidity_avg: float
    light_avg: float

    record_count: int



class WeatherAlert(BaseModel):
    type: str
    message: str
    value: float
    threshold: float
    severity: str


class AlertsResponse(BaseModel):
    status: str
    alerts: List[WeatherAlert]
    checked_at: datetime
    station_id: str


class PredictionPoint(BaseModel):
    hour: datetime
    temperature: float
    humidity: float


class PredictionResponse(BaseModel):
    station_id: str
    predictions: List[PredictionPoint]
    model: str
    based_on_records: int
    generated_at: datetime
    message: str