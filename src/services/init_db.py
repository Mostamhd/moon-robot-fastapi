from sqlalchemy.future import select

from src.models.database import Base, Obstacle
from src.services.database import AsyncSessionLocal, engine


async def init_db() -> None:
    """Initialize the database with default data"""
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Add default obstacles if none exist
    async with AsyncSessionLocal() as session, session.begin():
        # Check if obstacles already exist
        result = await session.execute(select(Obstacle))
        if result.scalars().first() is None:
            default_obstacles = [
                Obstacle(position_x=1, position_y=4),
                Obstacle(position_x=3, position_y=5),
                Obstacle(position_x=7, position_y=4),
            ]
            session.add_all(default_obstacles)
            await session.commit()
            print(f"Added {len(default_obstacles)} default\
                    obstacles to the database")

    print("Database initialization complete")


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())
