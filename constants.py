from enum import Enum, unique


@unique
class Move(Enum):
    FORWARD = 1
    BACKWARD = 2
    SPIN_RIGHT = 3
    SPIN_LEFT = 4


@unique
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


ACTION_BASE_COST = {
    Move.FORWARD: 1.0,
    Move.BACKWARD: 1.0,
    Move.SPIN_LEFT: 1.0,
    Move.SPIN_RIGHT: 1.0
}
