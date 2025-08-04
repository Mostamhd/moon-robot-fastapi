import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.router import api_router
from src.services.database import engine
from src.services.init_db import init_db as initialize_database
from src.settings import settings

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown events"""
    # Startup
    logger.info("Starting Moon Robot API")
    # Initialize database with default data
    try:
        await initialize_database()
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Moon Robot API")
    await engine.dispose()
    logger.info("Database engine disposed")


app = FastAPI(
    title="Moon Robot API",
    description="API for controlling a robot on the Moon",
    version="1.0.0",
    lifespan=lifespan,
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)
