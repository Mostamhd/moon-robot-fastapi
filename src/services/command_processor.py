import logging
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.robot import Direction, Position, Robot
from src.services.robot_service import RobotCommandExecutor

# Set up logger
logger = logging.getLogger(__name__)


class CommandProcessor:
    """Service for processing robot commands with obstacle detection"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.executor = RobotCommandExecutor()

    async def get_obstacles(self) -> set[Position]:
        """
        Get obstacles from database with proper error handling
        """
        from src.models.obstacle import Obstacle

        try:
            result = await self.db_session.execute(select(Obstacle))
            obstacles = result.scalars().all()
            return {
                Position(obstacle.position_x, obstacle.position_y)
                for obstacle in obstacles
            }
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching obstacles: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching obstacles: {e}")
            raise

    async def process_commands(
        self,
        command_string: str,
        start_position: tuple[int, int],
        start_direction: Direction,
    ) -> dict[str, Any]:
        """
        Process a command string and return the final robot state.
        Handles obstacle detection as specified in Part II.
        """
        try:
            # Validate command string
            if not isinstance(command_string, str):
                raise ValueError("Command string must be a string")

            robot = Robot(position=start_position, direction=start_direction)
            obstacles = await self.get_obstacles()
            return self.executor.execute_commands(robot, command_string, obstacles)
        except Exception as e:
            logger.error(f"Error processing commands '{command_string}': {e}")
            raise
