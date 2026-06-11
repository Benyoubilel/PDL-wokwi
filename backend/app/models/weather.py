from typing import Optional
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Weather(Base):
    __tablename__ = "weather"

    id:            Mapped[int]      = mapped_column(primary_key=True, index=True)
    station_id:    Mapped[str]      = mapped_column(String(100), index=True)
    temperature:   Mapped[float]    = mapped_column(Float)
    humidity:      Mapped[float]    = mapped_column(Float)
    light_raw:     Mapped[float]    = mapped_column(Float)
    light_percent: Mapped[float]    = mapped_column(Float)
    heat_index:    Mapped[float]    = mapped_column(Float)
    dew_point:     Mapped[float]    = mapped_column(Float)
    latitude:      Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude:     Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at:    Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )