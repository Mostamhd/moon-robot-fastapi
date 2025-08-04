import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str | None = None

    START_POSITION: str = os.getenv("START_POSITION", "(0, 0)")
    START_DIRECTION: str = os.getenv("START_DIRECTION", "NORTH")

    @field_validator("START_POSITION")
    def validate_start_position(cls, v: str) -> str:
        """Validate that START_POSITION is a valid tuple string."""
        if not v:
            raise ValueError("START_POSITION cannot be empty")

        try:
            import ast

            pos = ast.literal_eval(v)
            if not isinstance(pos, tuple) or len(pos) != 2:
                raise ValueError("START_POSITION must be a tuple of two integers")
            if not all(isinstance(coord, int) for coord in pos):
                raise ValueError("START_POSITION coordinates must be integers")
        except (SyntaxError, ValueError) as e:
            raise ValueError(
                f"Invalid START_POSITION format: {v}. "
                + f"Must be a tuple like '(0, 0)'. Error: {e!s}"
            ) from e

        return v

    @field_validator("START_DIRECTION")
    def validate_start_direction(cls, v: str) -> str:
        """Validate that START_DIRECTION is a valid direction."""
        valid_directions = {"NORTH", "SOUTH", "EAST", "WEST"}
        if v not in valid_directions:
            raise ValueError(f"START_DIRECTION must be one of {valid_directions}")
        return v

    @property
    def start_position(self) -> tuple[int, int]:
        """Parse START_POSITION string into a tuple safely."""
        import ast

        pos = ast.literal_eval(self.START_POSITION)
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

        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://robotuser:robotpass@localhost:5432/moonrobot",
        )

        # Ensure we're using the asyncpg driver
        if database_url.startswith("postgresql://") and not database_url.startswith(
            "postgresql+asyncpg://"
        ):
            database_url = database_url.replace(
                "postgresql://", "postgresql+asyncpg://", 1
            )

        return database_url


settings = Settings()
