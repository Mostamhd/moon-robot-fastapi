from enum import Enum
from typing import NamedTuple


class Direction(str, Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class Position(NamedTuple):
    x: int
    y: int


class Robot:
    def __init__(self, position: tuple[int, int], direction: Direction) -> None:
        self.position = Position(*position)
        self.direction = direction
        self.obstacle_detected = False

    def move_forward(self) -> None:
        x, y = self.position

        if self.direction == Direction.NORTH:
            y += 1
        elif self.direction == Direction.SOUTH:
            y -= 1
        elif self.direction == Direction.EAST:
            x += 1
        elif self.direction == Direction.WEST:
            x -= 1

        self.position = Position(x, y)

    def move_backward(self) -> None:
        x, y = self.position

        if self.direction == Direction.NORTH:
            y -= 1
        elif self.direction == Direction.SOUTH:
            y += 1
        elif self.direction == Direction.EAST:
            x -= 1
        elif self.direction == Direction.WEST:
            x += 1

        self.position = Position(x, y)

    def rotate_left(self) -> None:
        if self.direction == Direction.NORTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.NORTH

    def rotate_right(self) -> None:
        if self.direction == Direction.NORTH:
            self.direction = Direction.EAST
        elif self.direction == Direction.EAST:
            self.direction = Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            self.direction = Direction.WEST
        elif self.direction == Direction.WEST:
            self.direction = Direction.NORTH

    def process_command(self, command: str) -> bool:
        if command == "F":
            self.move_forward()
            return True
        if command == "B":
            self.move_backward()
            return True
        if command == "L":
            self.rotate_left()
            return False
        if command == "R":
            self.rotate_right()
            return False
        return False
