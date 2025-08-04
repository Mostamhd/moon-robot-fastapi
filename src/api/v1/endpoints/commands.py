from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.database import CommandHistory, RobotState
from src.models.robot import Direction, Robot
from src.services.command_processor import CommandProcessor
from src.services.database import get_db
from src.settings import settings

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

    response_data = {
        "position": {"x": x_position, "y": y_position},
        "direction": direction,
        "obstacle_detected": obstacle_detected,
    }
    return CommandResponse(**response_data)
