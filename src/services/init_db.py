import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from src.models.base import Base
from src.models.obstacle import Obstacle
from src.services.database import engine

logger = logging.getLogger(__name__)


async def init_db(custom_engine: AsyncEngine | None = None) -> None:
    """Initialize the database with default data"""
    db_engine = custom_engine or engine

    try:
        async with db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")

        from sqlalchemy.ext.asyncio import async_sessionmaker

        session_factory = async_sessionmaker(db_engine, expire_on_commit=False)

        async with session_factory() as session:
            try:
                async with session.begin():
                    result = await session.execute(select(Obstacle))
                    if result.scalars().first() is None:
                        default_obstacles = [
                            Obstacle(position_x=1, position_y=4),
                            Obstacle(position_x=3, position_y=5),
                            Obstacle(position_x=7, position_y=4),
                        ]
                        session.add_all(default_obstacles)
                        await session.commit()
                        logger.info(
                            f"Added {len(default_obstacles)} default obstacles "
                            + "to the database"
                        )
                    else:
                        logger.info(
                            "Obstacles already exist in database, "
                            + "skipping initialization"
                        )
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error while initializing obstacles: {e}")
                raise
            except Exception as e:
                await session.rollback()
                logger.error(f"Unexpected error while initializing obstacles: {e}")
                raise

        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())
