from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from src.models.database import CommandHistory, Obstacle, RobotState


@pytest.mark.asyncio
async def test_robot_state_defaults(async_db_session):
    robot = RobotState()
    async_db_session.add(robot)
    await async_db_session.commit()
    await async_db_session.refresh(robot)

    assert robot.position_x == 0
    assert robot.position_y == 0
    assert robot.direction == "NORTH"
    assert robot.created_at is not None
    assert robot.updated_at is not None


@pytest.mark.asyncio
async def test_command_history_defaults(async_db_session):
    entry = CommandHistory(command="F", position_x=1, position_y=1, direction="NORTH")
    async_db_session.add(entry)
    await async_db_session.commit()
    await async_db_session.refresh(entry)

    assert entry.command == "F"
    assert entry.obstacle_detected is False
    assert entry.executed_at is not None


@pytest.mark.asyncio
async def test_obstacle_unique_constraint(async_db_session):
    obs1 = Obstacle(position_x=2, position_y=3)
    obs2 = Obstacle(position_x=2, position_y=3)

    async_db_session.add_all([obs1, obs2])
    with pytest.raises(IntegrityError):
        await async_db_session.commit()


def test_robot_state_model():
    robot = RobotState()
    assert robot.position_x is None
    assert robot.position_y is None
    assert robot.direction is None
    assert isinstance(robot.created_at, datetime) or robot.created_at is None
    assert isinstance(robot.updated_at, datetime) or robot.updated_at is None

    robot = RobotState(position_x=1, position_y=2, direction="SOUTH")
    assert robot.position_x == 1
    assert robot.position_y == 2
    assert robot.direction == "SOUTH"


def test_command_history_model():
    command = CommandHistory(
        command="F",
        position_x=0,
        position_y=0,
        direction="NORTH",
    )
    assert command.command == "F"
    assert command.position_x == 0
    assert command.position_y == 0
    assert command.direction == "NORTH"
    assert command.obstacle_detected is None
    assert isinstance(command.executed_at, datetime) or command.executed_at is None

    command = CommandHistory(
        command="FFR",
        position_x=1,
        position_y=2,
        direction="EAST",
        obstacle_detected=True,
    )
    assert command.command == "FFR"
    assert command.position_x == 1
    assert command.position_y == 2
    assert command.direction == "EAST"
    assert command.obstacle_detected is True


def test_obstacle_model():
    obstacle = Obstacle(position_x=3, position_y=5)
    assert obstacle.position_x == 3
    assert obstacle.position_y == 5
    assert isinstance(obstacle.created_at, datetime) or obstacle.created_at is None


def test_robot_state_repr():
    robot = RobotState(id=1, position_x=1, position_y=2, direction="NORTH")
    assert isinstance(repr(robot), str)


def test_command_history_repr():
    command = CommandHistory(
        id=1,
        command="F",
        position_x=0,
        position_y=0,
        direction="NORTH",
    )
    assert isinstance(repr(command), str)


def test_obstacle_repr():
    obstacle = Obstacle(id=1, position_x=3, position_y=5)
    assert isinstance(repr(obstacle), str)
