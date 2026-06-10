from fastapi import FastAPI

from app.core.config import settings

from app.db.base import Base
from app.db.session import engine

from app.api.weather import router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

app.include_router(
    router,
    prefix=settings.API_PREFIX
)