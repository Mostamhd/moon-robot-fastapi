# Moon Robot API

## Overview
This API controls a robot on the Moon, translating commands from Earth to instructions the robot understands.

## Requirements
- Python 3.11+
- Docker 20.10+
- PostgreSQL 15+

## Setup

### Local Development with Docker

1. Ensure Docker and Docker Compose are installed
2. Start the services:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```
3. The API will be available at http://localhost:8000
4. API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development without Docker

1. Install UV:
   ```bash
   pip install uv
   ```
2. Create virtual environment and install dependencies:
   ```bash
   uv venv
   . .venv/bin/activate
   uv sync
   ```
3. Set up environment variables:
   ```bash
   echo "DATABASE_URL=postgresql+asyncpg://robotuser:robotpass@localhost:5432/moonrobot" > .env
   echo "START_POSITION=(0, 0)" >> .env
   echo "START_DIRECTION=NORTH" >> .env
   ```
4. Start PostgreSQL locally (using your preferred method)
5. Run the application:
   ```bash
   uv run uvicorn src.main:app --reload
   ```

## API Endpoints

### GET /api/v1/status
Returns the current position and direction of the robot.

Example response:
```json
{
  "position": {"x": 0, "y": 0},
  "direction": "NORTH"
}
```

### POST /api/v1/commands
Executes a command string and returns the final position.

Request body:
```json
{
  "command": "FLFFFRFLB"
}
```

Example response:
```json
{
  "position": {"x": -1, "y": 3},
  "direction": "NORTH",
  "obstacle_detected": false
}
```

When an obstacle is detected:
```json
{
  "position": {"x": 0, "y": 3},
  "direction": "WEST",
  "obstacle_detected": true,
}
```

## Testing

### Running Tests
```bash
uv run pytest
```

### Testing the API Manually

1. Check initial status:
   ```bash
   curl http://localhost:8000/api/v1/status
   ```

2. Send movement commands:
   ```bash
   curl -X POST http://localhost:8000/api/v1/commands \
     -H "Content-Type: application/json" \
     -d '{"command": "F"}'
   ```

3. Verify new position:
   ```bash
   curl http://localhost:8000/api/v1/status
   ```

4. Test obstacle detection (start at position (0,3) facing north):
   ```bash
   # To test from a specific position, restart the application with new environment variables:
   # START_POSITION="(0,3)" START_DIRECTION="NORTH" uvicorn src.main:app --reload

   # Try to move into obstacle at (0,4)
   curl -X POST http://localhost:8000/api/v1/commands \
     -H "Content-Type: application/json" \
     -d '{"command": "F"}'
   ```
   This should return with "obstacle_detected": true

## Code Quality

This project uses comprehensive quality checks:

- Ruff for Python linting and formatting
- mypy for static type checking
- Pre-commit hooks for automatic quality checks
- GitHub Actions for CI/CD pipeline

All code must pass these checks before merging.

## Database Migrations

This project uses Alembic for database migrations. See [alembic/README.md](alembic/README.md) for detailed information on how to work with migrations.

For development, it's recommended to run migrations using Docker to ensure consistency with the development environment:

```bash
# Apply all pending migrations
docker-compose -f docker/docker-compose.yml exec api alembic upgrade head

# Check current revision
docker-compose -f docker/docker-compose.yml exec api alembic current

# Create a new migration
docker-compose -f docker/docker-compose.yml exec api alembic revision --autogenerate -m "Description of changes"
```

After creating new migration files, you'll need to rebuild the Docker containers to include these files:

```bash
docker-compose -f docker/docker-compose.yml up --build -d
```

## Development Workflow

1. Make changes to the code
2. Run tests: `uv run pytest`
3. Check linting: `uv run ruff check .`
4. Check types: `uv run mypy .`
5. Commit changes with conventional commits

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency. The hooks automatically run:

- Ruff for Python linting and formatting
- mypy for static type checking
- Various checks for YAML files, trailing whitespace, etc.

### Installation

To install and set up pre-commit hooks:

1. Install pre-commit (if not already installed):
   ```bash
   uv add pre-commit
   ```

2. Install the git hook scripts:
   ```bash
   uv pre-commit install
   ```

### Usage

The pre-commit hooks will automatically run on every commit. You can also manually run them on all files:

```bash
uv run pre-commit run --all-files
```

If any hooks fail, fix the issues and try committing again. Some hooks (like Ruff) may automatically fix issues, so you might just need to stage the fixed files and commit again.

## Configuration

The robot can be configured using environment variables:

- `START_POSITION`: Initial position as "(x, y)" (default: "(0, 0)")
- `START_DIRECTION`: Initial direction (NORTH, SOUTH, EAST, WEST) (default: "NORTH")
- `DATABASE_URL`: PostgreSQL connection string
