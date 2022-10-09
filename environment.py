from typing import Dict, List, Tuple

import cv2
import numpy as np

import constants
from cell import Cell


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

    def render(self):
        cell_size = (100, 100)
        border_width = 2
        self._image = np.zeros((*cell_size, 3), dtype=np.uint8)
        for i in range(self.n_rows):
            row_image = None
            for j in range(self.n_cols):
                if (i, j) == self.start_position:
                    R, G, B = 200, 20, 20
                elif (i, j) == self.goal_position:
                    R, G, B = 20, 200, 20
                elif (i, j) in self.obstacle_positions:
                    R, G, B = 20, 20, 20
                else:
                    R, G, B = 128, 128, 128
                b = np.full(cell_size, B)
                g = np.full(cell_size, G)
                r = np.full(cell_size, R)
                cell_image = cv2.merge((b, g, r))
                cell_image[:, :border_width, :] = (255, 255, 255)
                cell_image[:border_width, :, :] = (255, 255, 255)
                cell_image[-border_width:, :, :] = (255, 255, 255)
                cell_image[:, -border_width:, :] = (255, 255, 255)

                if (i, j) == self.agent_position:
                    cv2.circle(cell_image,
                               (cell_size[0] // 2, cell_size[1] // 2),
                               min(cell_size) // 4,
                               (255, 20, 20),
                               -1)

                if j == 0:
                    row_image = cell_image
                else:
                    row_image = np.hstack((row_image, cell_image))
            if i == 0:
                self._image = row_image
            else:
                self._image = np.vstack((self._image, row_image))
        self._image = self._image.astype(np.uint8)
        print(f'{self._image.dtype}, {self._image.shape}')
        cv2.imshow('output', self._image)
        cv2.waitKey(0)


def main():
    filename = 'testcases/ex1.txt'
    env = Environment(filename=filename)
    assert env.start_position is not None
    assert env.drift_ccw_probabilities is not None
    assert env.drift_cw_probabilities is not None
    env.render()


if __name__ == '__main__':
    main()
