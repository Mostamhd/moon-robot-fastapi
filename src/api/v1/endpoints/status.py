from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.database import RobotState
from src.services.database import get_db
from src.settings import settings

DBSession = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter()


@router.get("/status")
async def get_status(db: DBSession) -> dict[str, Any]:
    result = await db.execute(
        select(RobotState).order_by(RobotState.updated_at.desc()).limit(1)
    )
    robot_state = result.scalars().first()

    if not robot_state:
        return {
            "position": {
                "x": settings.start_position[0],
                "y": settings.start_position[1],
            },
            "direction": settings.start_direction,
        }

    return {
        "position": {"x": robot_state.position_x, "y": robot_state.position_y},
        "direction": robot_state.direction,
    }
