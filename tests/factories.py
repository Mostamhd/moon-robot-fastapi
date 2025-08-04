import factory
from factory import fuzzy

from src.models.command_history import CommandHistory
from src.models.obstacle import Obstacle
from src.models.robot_state import RobotState


class RobotStateFactory(factory.Factory):
    class Meta:
        model = RobotState

    position_x = factory.Faker("pyint", min_value=-100, max_value=100)
    position_y = factory.Faker("pyint", min_value=-100, max_value=100)
    direction = fuzzy.FuzzyChoice(["NORTH", "SOUTH", "EAST", "WEST"])


class CommandHistoryFactory(factory.Factory):
    class Meta:
        model = CommandHistory

    command = fuzzy.FuzzyChoice(["F", "B", "L", "R", "FF", "FLFFFRFLB"])
    position_x = factory.Faker("pyint", min_value=-100, max_value=100)
    position_y = factory.Faker("pyint", min_value=-100, max_value=100)
    direction = fuzzy.FuzzyChoice(["NORTH", "SOUTH", "EAST", "WEST"])
    obstacle_detected = factory.Faker("boolean")


class ObstacleFactory(factory.Factory):
    class Meta:
        model = Obstacle

    position_x = factory.Faker("pyint", min_value=-50, max_value=50)
    position_y = factory.Faker("pyint", min_value=-50, max_value=50)

    @classmethod
    def create_batch_unique_positions(cls, size: int, **kwargs):
        obstacles: list[Obstacle] = []
        positions = set()

        while len(obstacles) < size:
            obstacle = cls(**kwargs)
            position = (obstacle.position_x, obstacle.position_y)

            if position not in positions:
                positions.add(position)
                obstacles.append(obstacle)

        return obstacles
