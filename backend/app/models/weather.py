from datetime import datetime

from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from app.db.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    station_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    temperature: Mapped[float] = mapped_column(Float)

    humidity: Mapped[float] = mapped_column(Float)

    light_raw: Mapped[float] = mapped_column(Float)

    light_percent: Mapped[float] = mapped_column(Float)

    heat_index: Mapped[float] = mapped_column(Float)

    dew_point: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )