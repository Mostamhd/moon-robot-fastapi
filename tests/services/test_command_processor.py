from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models.robot import Direction
from src.services.command_processor import CommandProcessor


@pytest.mark.asyncio
async def test_command_processor_initialization():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)
    assert processor.db_session == mock_db_session


@pytest.mark.asyncio
async def test_process_valid_commands():
    """Test processing valid command strings"""
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        result = await processor.process_commands(
            command_string="F", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 1
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_process_rotation_commands():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        result = await processor.process_commands(
            command_string="L", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["direction"] == Direction.WEST

        result = await processor.process_commands(
            command_string="R", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["direction"] == Direction.EAST


@pytest.mark.asyncio
async def test_process_obstacle_detection():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = {(0, 1)}

        result = await processor.process_commands(
            command_string="F", start_position=(0, 0), start_direction=Direction.NORTH
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 0
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is True


@pytest.mark.asyncio
async def test_process_complex_command_sequence():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        result = await processor.process_commands(
            command_string="FFRLB",
            start_position=(0, 0),
            start_direction=Direction.NORTH,
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 1
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_process_commands_with_multiple_obstacles():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = {(0, 1), (1, 1), (1, 0)}

        result = await processor.process_commands(
            command_string="FRF",
            start_position=(0, 0),
            start_direction=Direction.NORTH,
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 0
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is True


@pytest.mark.asyncio
async def test_process_empty_command_string():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        result = await processor.process_commands(
            command_string="", start_position=(5, 3), start_direction=Direction.EAST
        )
        assert result["position"]["x"] == 5
        assert result["position"]["y"] == 3
        assert result["direction"] == Direction.EAST
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_process_commands_with_invalid_characters():
    mock_db_session = AsyncMock()
    processor = CommandProcessor(mock_db_session)

    with patch.object(
        processor, "get_obstacles", new_callable=AsyncMock
    ) as mock_get_obstacles:
        mock_get_obstacles.return_value = set()

        result = await processor.process_commands(
            command_string="FXF",
            start_position=(0, 0),
            start_direction=Direction.NORTH,
        )
        assert result["position"]["x"] == 0
        assert result["position"]["y"] == 2
        assert result["direction"] == Direction.NORTH
        assert result["obstacle_detected"] is False


@pytest.mark.asyncio
async def test_get_obstacles_from_database():
    mock_db_session = AsyncMock()

    mock_obstacles = [
        type("Obstacle", (), {"position_x": 1, "position_y": 4}),
        type("Obstacle", (), {"position_x": 3, "position_y": 5}),
        type("Obstacle", (), {"position_x": 7, "position_y": 4}),
    ]

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_obstacles

    mock_db_session.execute.return_value = mock_result

    processor = CommandProcessor(mock_db_session)
    obstacles = await processor.get_obstacles()

    expected_obstacles = {(1, 4), (3, 5), (7, 4)}
    assert obstacles == expected_obstacles

    mock_db_session.execute.assert_awaited_once()
