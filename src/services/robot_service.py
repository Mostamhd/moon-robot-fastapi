from typing import Any

from src.models.robot import Position, Robot


class RobotCommandExecutor:
    @staticmethod
    def execute_commands(
        robot: Robot, commands: str, obstacles: set[Position] | None = None
    ) -> dict[str, Any]:
        """
        Execute a string of commands on a robot.
        Returns a status dictionary with final position, direction,
        and obstacle information.
        """
        if obstacles is None:
            obstacles = set()

        for command in commands:
            prev_position = robot.position

            moved = robot.process_command(command)

            if moved and robot.position in obstacles:
                robot.position = prev_position
                robot.obstacle_detected = True
                return {
                    "position": {"x": robot.position.x, "y": robot.position.y},
                    "direction": robot.direction.value,
                    "obstacle_detected": True,
                }

        return {
            "position": {"x": robot.position.x, "y": robot.position.y},
            "direction": robot.direction.value,
            "obstacle_detected": robot.obstacle_detected,
        }
