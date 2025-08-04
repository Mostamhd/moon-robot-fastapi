from tests.factories import CommandHistoryFactory, ObstacleFactory, RobotStateFactory


def test_robot_state_factory():
    robot_state = RobotStateFactory()
    assert isinstance(robot_state.position_x, int)
    assert isinstance(robot_state.position_y, int)

    direction_str = str(robot_state.direction)
    assert direction_str in ["NORTH", "SOUTH", "EAST", "WEST"]


def test_command_history_factory():
    command_history = CommandHistoryFactory()

    command_str = str(command_history.command)
    assert isinstance(command_str, str)
    assert isinstance(command_history.position_x, int)
    assert isinstance(command_history.position_y, int)

    direction_str = str(command_history.direction)
    assert direction_str in ["NORTH", "SOUTH", "EAST", "WEST"]
    assert isinstance(command_history.obstacle_detected, bool)


def test_obstacle_factory():
    obstacle = ObstacleFactory()
    assert isinstance(obstacle.position_x, int)
    assert isinstance(obstacle.position_y, int)


def test_obstacle_factory_unique_positions():
    obstacles = ObstacleFactory.create_batch_unique_positions(5)
    assert len(obstacles) == 5

    positions = [(obs.position_x, obs.position_y) for obs in obstacles]
    assert len(positions) == len(set(positions))
