from datetime import datetime

from sqlalchemy import DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Obstacle(Base):
    """Tracks obstacles on the Moon surface"""

    __tablename__ = "obstacles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        # Ensure unique positions
        UniqueConstraint("position_x", "position_y", name="uq_obstacle_position"),
    )
