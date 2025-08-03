import pytest

from src.models.robot import Direction, Robot


def test_robot_initialization():
    robot = Robot((0, 0), Direction.NORTH)
    assert robot.position.x == 0
    assert robot.position.y == 0
    assert robot.direction == Direction.NORTH
    assert robot.obstacle_detected is False


@pytest.mark.parametrize(
    "initial_direction,expected_position",
    [
        (Direction.NORTH, (0, 1)),
        (Direction.SOUTH, (0, -1)),
        (Direction.EAST, (1, 0)),
        (Direction.WEST, (-1, 0)),
    ],
)
def test_robot_move_forward(initial_direction, expected_position):
    robot = Robot((0, 0), initial_direction)
    robot.move_forward()
    assert robot.position == expected_position


@pytest.mark.parametrize(
    "initial_direction,expected_position",
    [
        (Direction.NORTH, (0, -1)),
        (Direction.SOUTH, (0, 1)),
        (Direction.EAST, (-1, 0)),
        (Direction.WEST, (1, 0)),
    ],
)
def test_robot_move_backward(initial_direction, expected_position):
    robot = Robot((0, 0), initial_direction)
    robot.move_backward()
    assert robot.position == expected_position


@pytest.mark.parametrize(
    "initial,expected",
    [
        (Direction.NORTH, Direction.WEST),
        (Direction.WEST, Direction.SOUTH),
        (Direction.SOUTH, Direction.EAST),
        (Direction.EAST, Direction.NORTH),
    ],
)
def test_rotate_left(initial, expected):
    robot = Robot((0, 0), initial)
    robot.rotate_left()
    assert robot.direction == expected


@pytest.mark.parametrize(
    "initial,expected",
    [
        (Direction.NORTH, Direction.EAST),
        (Direction.EAST, Direction.SOUTH),
        (Direction.SOUTH, Direction.WEST),
        (Direction.WEST, Direction.NORTH),
    ],
)
def test_rotate_right(initial, expected):
    robot = Robot((0, 0), initial)
    robot.rotate_right()
    assert robot.direction == expected


def test_process_valid_commands():
    robot = Robot((0, 0), Direction.NORTH)

    moved = robot.process_command("F")
    assert moved is True
    assert robot.position == (0, 1)

    moved = robot.process_command("B")
    assert moved is True
    assert robot.position == (0, 0)

    moved = robot.process_command("L")
    assert moved is False
    result = robot.direction
    assert result == Direction.WEST

    moved = robot.process_command("R")
    assert moved is False
    assert robot.direction == Direction.NORTH


def test_process_invalid_command():
    robot = Robot((0, 0), Direction.NORTH)
    moved = robot.process_command("X")
    assert moved is False
    assert robot.position == (0, 0)
    assert robot.direction == Direction.NORTH


def test_execute_commands_simple():
    robot = Robot((0, 0), Direction.NORTH)
    result = robot.execute_commands("FF")
    assert result["position"] == {"x": 0, "y": 2}
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] is False


def test_execute_commands_complex():
    robot = Robot((0, 0), Direction.NORTH)
    result = robot.execute_commands("FFRFLB")
    assert result["position"] == {"x": 1, "y": 1}
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] is False


def test_execute_commands_with_obstacle():
    robot = Robot((0, 0), Direction.NORTH)
    from src.models.robot import Position

    result = robot.execute_commands("F", obstacles={Position(0, 1)})
    assert result["position"] == {"x": 0, "y": 0}
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] is True


def test_execute_commands_obstacle_mid_sequence():
    robot = Robot((0, 0), Direction.NORTH)
    from src.models.robot import Position

    result = robot.execute_commands("FFFR", obstacles={Position(0, 2)})
    assert result["position"] == {"x": 0, "y": 1}
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] is True


def test_execute_empty_commands():
    robot = Robot((5, 3), Direction.EAST)
    result = robot.execute_commands("")
    assert result["position"] == {"x": 5, "y": 3}
    assert result["direction"] == Direction.EAST
    assert result["obstacle_detected"] is False


def test_execute_commands_with_invalid_characters():
    robot = Robot((0, 0), Direction.NORTH)
    result = robot.execute_commands("FXF")
    assert result["position"] == {"x": 0, "y": 2}
    assert result["direction"] == Direction.NORTH
    assert result["obstacle_detected"] is False
