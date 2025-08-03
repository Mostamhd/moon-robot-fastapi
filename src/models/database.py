from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


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


class Obstacle(Base):
    """Tracks obstacles on the Moon surface"""

    __tablename__ = "obstacles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("position_x", "position_y", name="uq_obstacle_position"),
    )
