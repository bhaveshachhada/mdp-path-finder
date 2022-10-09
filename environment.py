from typing import Dict, List, Tuple

import constants
from cell import Cell


class Environment:

    def __init__(self, filename):

        self._filename = filename

        self.n_rows: int = None
        self.n_cols: int = None

        self._grid: List[List[Cell]] = None

        self.start_position: Tuple[int, int, constants.Direction] = None
        self.goal_position: Tuple[int, int, constants.Direction] = None
        self.n_obstacles: int = None
        self.obstacle_positions: List[Tuple[int, int]] = None

        self.double_move_probabilities: Dict[constants.Move: float] = None
        self.drift_cw_probabilities: Dict[constants.Move: float] = None
        self.drift_ccw_probabilities: Dict[constants.Move: float] = None

        self.collision_penalty: float = None

        self._read_environment_config()
        self._generate_grid()

    def _read_environment_config(self):
        f = open(self._filename, 'r')

        for line in f:

            if line:

                if line.startswith("#"):
                    continue

                obstacles = list()
                count = 1

                if self.n_rows is None:
                    m, n = list(map(int, input().split(',')))
                    self.n_rows, self.n_cols = m, n

                elif self.start_position is None:
                    m, n = list(map(int, input().split(',')))
                    self.start_position = (m, n)

                elif self.goal_position is None:
                    m, n = list(map(int, input().split(',')))
                    self.goal_position = (m, n)

                elif self.n_obstacles is None:
                    self.n_obstacles = int(input())

                elif count < self.n_obstacles:
                    m, n = list(map(int, input().split(',')))
                    self.obstacle_positions.append((m, n))

    def _generate_grid(self):
        for i in range(self.n_rows):
            row = list()
            for j in range(self.n_cols):
                cell = Cell(row=i, column=j)
                row.append(cell)
            self._grid.append(row)
