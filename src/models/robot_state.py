from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class RobotState(Base):
    """Tracks the current state of the robot"""

    __tablename__ = "robot_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    position_x: Mapped[int] = mapped_column(Integer, default=0)
    position_y: Mapped[int] = mapped_column(Integer, default=0)
    direction: Mapped[str] = mapped_column(String(10), default="NORTH")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
