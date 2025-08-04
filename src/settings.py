import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str | None = None

    START_POSITION: str = os.getenv("START_POSITION", "(0, 0)")
    START_DIRECTION: str = os.getenv("START_DIRECTION", "NORTH")

    @property
    def start_position(self) -> tuple[int, int]:
        """Parse START_POSITION string into a tuple safely."""
        import ast

        pos = ast.literal_eval(self.START_POSITION)
        assert isinstance(pos, tuple) and len(pos) == 2
        return (int(pos[0]), int(pos[1]))  # Explicit type conversion

    @property
    def start_direction(self) -> str:
        return self.START_DIRECTION

    @property
    def database_url(self) -> str:
        """Return the database URL based on environment"""
        in_docker = (
            Path("/.dockerenv").exists() or os.getenv("DOCKER_ENV", "false") == "true"
        )

        if in_docker:
            return "postgresql+asyncpg://robotuser:robotpass@db:5432/moonrobot"
        return os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://robotuser:robotpass@localhost:5432/moonrobot",
        )


settings = Settings()
