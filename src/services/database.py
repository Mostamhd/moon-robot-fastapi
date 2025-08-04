import logging
from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

# Set up logger
logger = logging.getLogger(__name__)


try:
    engine = create_async_engine(
        settings.database_url,
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        echo=False,
        pool_pre_ping=True,
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error in database session: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
