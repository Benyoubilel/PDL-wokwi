from pydantic import BaseModel
from pydantic import Field
from datetime import datetime


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

    created_at: datetime

    model_config = {
        "from_attributes": True
    }