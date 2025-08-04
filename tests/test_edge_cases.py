from src.models.robot import Direction, Position, Robot
from src.services.robot_service import RobotCommandExecutor


def test_robot_at_boundary_positions():
    robot = Robot((0, 0), Direction.NORTH)
    executor = RobotCommandExecutor()
    result = executor.execute_commands(robot, "F")
    assert result["position"] == {"x": 0, "y": 1}

    robot = Robot((-5, -3), Direction.NORTH)
    result = executor.execute_commands(robot, "F")
    assert result["position"] == {"x": -5, "y": -2}


def test_robot_complex_rotation_sequences():
    robot = Robot((0, 0), Direction.NORTH)
    executor = RobotCommandExecutor()

    result = executor.execute_commands(robot, "LLLL")
    assert result["direction"] == "NORTH"
    assert result["position"] == {"x": 0, "y": 0}

    robot = Robot((0, 0), Direction.NORTH)
    result = executor.execute_commands(robot, "RRRR")
    assert result["direction"] == "NORTH"
    assert result["position"] == {"x": 0, "y": 0}


def test_robot_movement_with_multiple_obstacles():
    robot = Robot((0, 0), Direction.NORTH)
    executor = RobotCommandExecutor()

    obstacles = {Position(0, 1), Position(0, 2)}

    result = executor.execute_commands(robot, "FF", obstacles=obstacles)
    assert result["position"] == {"x": 0, "y": 0}
    assert result["obstacle_detected"] is True


def test_robot_movement_with_adjacent_obstacles():
    robot = Robot((0, 0), Direction.EAST)
    executor = RobotCommandExecutor()

    obstacles = {Position(1, 1)}

    result = executor.execute_commands(robot, "F", obstacles=obstacles)
    assert result["position"] == {"x": 1, "y": 0}
    assert result["obstacle_detected"] is False


def test_empty_and_invalid_command_strings():
    robot = Robot((0, 0), Direction.NORTH)
    executor = RobotCommandExecutor()

    result = executor.execute_commands(robot, "")
    assert result["position"] == {"x": 0, "y": 0}
    assert result["direction"] == "NORTH"
    assert result["obstacle_detected"] is False

    result = executor.execute_commands(robot, "XXXX")
    assert result["position"] == {"x": 0, "y": 0}
    assert result["direction"] == "NORTH"
    assert result["obstacle_detected"] is False


def test_robot_state_persistence_after_obstacle_detection():
    robot = Robot((0, 0), Direction.NORTH)
    executor = RobotCommandExecutor()

    obstacles = {Position(0, 2)}

    result1 = executor.execute_commands(robot, "F")
    assert result1["position"] == {"x": 0, "y": 1}
    assert result1["direction"] == "NORTH"

    robot2 = Robot((0, 1), Direction.NORTH)

    result2 = executor.execute_commands(robot2, "F", obstacles=obstacles)
    assert result2["position"] == {"x": 0, "y": 1}
    assert result2["direction"] == "NORTH"
    assert result2["obstacle_detected"] is True


def test_consecutive_obstacle_encounters():
    robot = Robot((0, 0), Direction.NORTH)
    executor = RobotCommandExecutor()

    obstacles = {Position(0, 1), Position(0, 2)}

    result1 = executor.execute_commands(robot, "F", obstacles=obstacles)
    assert result1["position"] == {"x": 0, "y": 0}
    assert result1["obstacle_detected"] is True
