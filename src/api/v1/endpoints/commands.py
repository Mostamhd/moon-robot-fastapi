import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Direction, Robot
from src.models.command_history import CommandHistory
from src.models.robot_state import RobotState
from src.services.command_processor import CommandProcessor
from src.services.database import get_db
from src.settings import settings

logger = logging.getLogger(__name__)

DBSession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter()


class CommandRequest(BaseModel):
    command: str


class CommandResponse(BaseModel):
    position: dict[str, int]
    direction: str
    obstacle_detected: bool = False


@router.post("/commands", response_model=CommandResponse)
async def execute_commands(request: CommandRequest, db: DBSession) -> CommandResponse:
    """
    Execute a string of commands and return the final position.
    """
    try:
        if len(request.command) > 1000:
            raise HTTPException(status_code=400, detail="Command string too long")

        stmt = select(RobotState).order_by(RobotState.updated_at.desc()).limit(1)
        result = await db.execute(stmt)
        robot_state = result.scalars().first()

        if not robot_state:
            start_position = settings.start_position
            start_direction = Direction[settings.start_direction]
            robot = Robot(position=start_position, direction=start_direction)
        else:
            robot = Robot(
                position=(robot_state.position_x, robot_state.position_y),
                direction=Direction[robot_state.direction],
            )

        command_processor = CommandProcessor(db)
        command_result = await command_processor.process_commands(
            request.command, (robot.position.x, robot.position.y), robot.direction
        )

        x_position = command_result["position"]["x"]
        y_position = command_result["position"]["y"]
        direction = command_result["direction"]
        obstacle_detected = command_result["obstacle_detected"]

        try:
            command_history = CommandHistory(
                command=request.command,
                position_x=x_position,
                position_y=y_position,
                direction=direction,
                obstacle_detected=obstacle_detected,
            )
            db.add(command_history)

            if not robot_state:
                robot_state = RobotState(
                    position_x=x_position, position_y=y_position, direction=direction
                )
                db.add(robot_state)
            else:
                robot_state.position_x = x_position
                robot_state.position_y = y_position
                robot_state.direction = direction

            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving command history: {e}")
            raise HTTPException(
                status_code=500, detail="Failed to save command history"
            ) from e

        response_data = {
            "position": {"x": x_position, "y": y_position},
            "direction": direction,
            "obstacle_detected": obstacle_detected,
        }
        return CommandResponse(**response_data)

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error executing commands: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
