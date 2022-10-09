from enum import Enum, unique


@unique
class Move(Enum):
    UP = 1
    DOWN = 2
    SPIN_RIGHT = 3
    SPIN_LEFT = 4


ACTION_BASE_COST = {
    Move.UP: 1.0,
    Move.DOWN: 1.0,
    Move.SPIN_LEFT: 1.0,
    Move.SPIN_RIGHT: 1.0
}
