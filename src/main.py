from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.router import api_router
from src.services.database import engine
from src.services.init_db import init_db as initialize_database
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown events"""
    # Startup
    # TODO add a logger here
    # Initialize database with default data
    await initialize_database()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="Moon Robot API",
    description="API for controlling a robot on the Moon",
    version="1.0.0",
    lifespan=lifespan,
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)
