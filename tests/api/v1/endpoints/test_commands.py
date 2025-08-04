# test_commands.py
import pytest
from sqlalchemy import select

from src.models.database import CommandHistory, Obstacle


@pytest.mark.asyncio
async def test_execute_commands_success(client):
    response = await client.post("/api/v1/commands", json={"command": "F"})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 1}
    assert data["direction"] == "NORTH"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_execute_commands_with_rotation(client):
    response = await client.post("/api/v1/commands", json={"command": "RFF"})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 2, "y": 0}
    assert data["direction"] == "EAST"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_execute_commands_with_obstacle(client, async_db_session):
    # Insert an obstacle at (0,2)
    obstacle = Obstacle(position_x=0, position_y=2)

    async_db_session.add(obstacle)
    await async_db_session.commit()
    await async_db_session.refresh(obstacle)

    response = await client.post("/api/v1/commands", json={"command": "FFF"})
    assert response.status_code == 200
    data = response.json()
    # Robot stops before obstacle at (0,2), so final pos is (0,1)
    assert data["position"] == {"x": 0, "y": 1}
    assert data["direction"] == "NORTH"
    assert data["obstacle_detected"] is True


@pytest.mark.asyncio
async def test_execute_commands_invalid_command(client):
    response = await client.post("/api/v1/commands", json={"command": "X"})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 0}
    assert data["direction"] == "NORTH"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_execute_commands_empty_command(client):
    response = await client.post("/api/v1/commands", json={"command": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["position"] == {"x": 0, "y": 0}
    assert data["direction"] == "NORTH"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_execute_commands_complex_sequence(client):
    response = await client.post("/api/v1/commands", json={"command": "FRFRLF"})
    assert response.status_code == 200
    data = response.json()

    assert data["position"] == {"x": 2, "y": 1}
    assert data["direction"] == "EAST"
    assert data["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_command_history_is_recorded(client, async_db_session):
    await client.post("/api/v1/commands", json={"command": "FFR"})

    result = await async_db_session.execute(
        select(CommandHistory).order_by(CommandHistory.id.desc())
    )
    command_entry = result.scalar_one_or_none()

    assert command_entry is not None
    assert command_entry.command == "FFR"
    assert command_entry.position_x == 0
    assert command_entry.position_y == 2
    assert command_entry.direction == "EAST"
