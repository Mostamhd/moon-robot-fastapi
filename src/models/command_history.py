from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class CommandHistory(Base):
    """Tracks all commands sent to the robot"""

    __tablename__ = "command_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    command: Mapped[str] = mapped_column(Text, nullable=False)
    position_x: Mapped[int | None] = mapped_column(Integer)
    position_y: Mapped[int | None] = mapped_column(Integer)
    direction: Mapped[str | None] = mapped_column(String(10))
    obstacle_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
