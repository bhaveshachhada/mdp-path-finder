from typing import Dict, List, Tuple

import cv2
import numpy as np

import constants
from cell import Cell


def manhattan(pt1, pt2):
    distance = 0
    for a, b in zip(pt1, pt2):
        distance += abs(a - b)
    return distance


class Environment:

    def __init__(self, filename):

        self._filename = filename

        self.n_rows: int = None
        self.n_cols: int = None

        self._grid: List[List[Cell]] = None

        self.start_position: Tuple[int, int] = None
        self.goal_position: Tuple[int, int] = None
        self.n_obstacles: int = None
        self.obstacle_positions: List[Tuple[int, int]] = list()

        self.double_move_probabilities: Dict[constants.Move: float] = None
        self.drift_cw_probabilities: Dict[constants.Move: float] = None
        self.drift_ccw_probabilities: Dict[constants.Move: float] = None

        self.collision_penalty: float = None

        self._read_environment_config()
        self._generate_grid()

        self.agent_position = self.start_position

        self._image = None
        # self.render()

    def _read_environment_config(self):
        f = open(self._filename, 'r')

        count = 0

        for line in f:

            if line:

                if line.startswith("#") or line == '\n':
                    continue

                if self.n_rows is None:
                    m, n = list(map(int, line.split(',')))
                    self.n_rows, self.n_cols = m, n

                elif self.start_position is None:
                    m, n = list(map(int, line.split(',')))
                    self.start_position = (m, n)

                elif self.goal_position is None:
                    m, n = list(map(int, line.split(',')))
                    self.goal_position = (m, n)

                elif self.n_obstacles is None:
                    self.n_obstacles = int(line)

                elif count < self.n_obstacles:
                    m, n = list(map(int, line.split(',')))
                    self.obstacle_positions.append((m, n))
                    count += 1

                elif self.double_move_probabilities is None:
                    self.double_move_probabilities = dict()
                    probs = list(map(float, line.split(',')))
                    for key, value in zip(constants.Move, probs):
                        self.double_move_probabilities[key] = value

                elif self.drift_cw_probabilities is None:
                    self.drift_cw_probabilities = dict()
                    probs = list(map(float, line.split(',')))
                    for key, value in zip(constants.Move, probs):
                        self.drift_cw_probabilities[key] = value

                elif self.drift_ccw_probabilities is None:
                    self.drift_ccw_probabilities = dict()
                    probs = list(map(float, line.split(',')))
                    for key, value in zip(constants.Move, probs):
                        self.drift_ccw_probabilities[key] = value

    def _generate_grid(self):
        self._grid = list()
        for i in range(self.n_rows):
            row = list()
            for j in range(self.n_cols):
                cell = Cell(row=i, column=j)
                row.append(cell)
            self._grid.append(row)

    def get_all_states(self) -> List[Cell]:
        states = list()
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if (i, j) not in self.obstacle_positions:
                    states.append(self._grid[i][j])
        return states

    def get_start_state(self) -> Cell:
        i, j = self.start_position
        return self._grid[i][j]

    def get_goal_state(self) -> Cell:
        i, j = self.goal_position
        return self._grid[i][j]

    def apply_dynamics(self, state: Cell, action: constants.Move) -> Tuple[float, Cell]:
        i, j = state.row, state.column

        y, x = i, j
        if action == constants.Move.UP:
            y = max(0, i - 1)
        elif action == constants.Move.DOWN:
            y = min(self.n_rows - 1, i + 1)
        elif action == constants.Move.LEFT:
            x = max(0, j - 1)
        elif action == constants.Move.RIGHT:
            x = min(self.n_cols - 1, j + 1)

        if (y, x) == self.goal_position:
            return 100, Cell(y, x)

        if (y, x) in self.obstacle_positions:
            return -100, Cell(y, x)

        else:
            goal = self.get_goal_state()
            next_state = Cell(y, x)
            return state.distance(goal) - next_state.distance(goal), next_state


def main():
    filename = 'testcases/ex1.txt'
    env = Environment(filename=filename)
    assert env.start_position is not None
    assert env.drift_ccw_probabilities is not None
    assert env.drift_cw_probabilities is not None
    # env.render()


if __name__ == '__main__':
    main()
