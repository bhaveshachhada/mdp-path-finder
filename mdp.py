import math
from collections import defaultdict
from typing import Dict, List

import cv2
import numpy as np

import constants
from cell import Cell
from environment import Environment


class MDPSolver:

    def __init__(self, environment: Environment):
        self.env = environment


class PolicyIterationSolver(MDPSolver):

    GAMMA = -0.1

    def __init__(self, environment: Environment):
        MDPSolver.__init__(self, environment)
        self._converged = False

        self._policy: Dict[Cell, constants.Move] = None
        self._state_space: List[Cell] = self.env.get_all_states()
        self._start_state: Cell = self.env.get_start_state()
        self._goal_state: Cell = self.env.get_goal_state()
        self._state_value: Dict[Cell, float] = None
        self._state_transition_probability: Dict[Cell, Dict[constants.Move, Dict[Cell, float]]] = None
        self._state_rewards: Dict[Cell, Dict[constants.Move, Dict[Cell, float]]] = None

        self._image = None

    def initialise(self):
        self._policy = defaultdict(lambda: constants.Move.FORWARD)
        self._state_value = defaultdict(lambda: 0.0)
        self._calculate_state_transition_probability()

    def iterate(self):
        while not self.converged:
            self.evaluate()
            self.improvise()

    def calculate_state_value(self, state: Cell):
        action = self._policy[state]
        return sum(self._state_transition_probability[state][action][next_state] *
                   (self._state_rewards[state][action][next_state] +
                    (self.GAMMA * self._state_value[next_state]))
                   for next_state in self._state_transition_probability[state][action])

    def evaluate(self):
        delta_max = math.inf
        iteration = 0
        while delta_max > 1e-3:
            deltas = list()
            for state in self._state_space:
                if state == self._goal_state:
                    continue
                value_s = self._state_value[state]
                value_s_prime = self.calculate_state_value(state)
                delta = abs(value_s - value_s_prime)
                self._state_value[state] = value_s_prime
                deltas.append(delta)
            iteration += 1
            delta_max = max(deltas)
            if iteration == 1000:
                break

    def improvise(self):
        self._converged = True
        for state in self._state_space:
            if state == self._goal_state:
                continue
            past_policy_action = self._policy[state]
            new_policy_action = self.select_best_move_from_state_values(state)
            if past_policy_action != new_policy_action:
                self._converged = False
            self._policy[state] = new_policy_action

    def select_best_move_from_state_values(self, state: Cell):
        formula = lambda s, action: sum(self._state_transition_probability[s][action][next_state] *
                                        (self._state_rewards[next_state] +
                                         (self.GAMMA * self._state_value[next_state]))
                                        for next_state in self._state_transition_probability[s][action])
        return max(list(constants.Move), key=lambda x: formula(state, x))

    @property
    def converged(self) -> bool:
        return self._converged

    def _calculate_state_transition_probability(self):
        self._state_transition_probability = dict()
        self._state_rewards = dict()
        for state in self._state_space:
            self._state_transition_probability[state] = dict()
            self._state_rewards = dict()
            for action in constants.Move:
                self._state_transition_probability[state][action] = defaultdict(lambda: 0.0)
                self._state_rewards[state][action] = defaultdict(lambda: 0.0)
                reward, new_state = self.env.apply_dynamics(state, action)
                self._state_transition_probability[state][action][new_state] = 1.0
                self._state_rewards[state][action][new_state] = reward

    def render(self):
        cell_size = (100, 100)
        border_width = 2
        self._image = np.zeros((*cell_size, 3), dtype=np.uint8)
        for i in range(self.env.n_rows):
            row_image = None
            for j in range(self.env.n_cols):
                if (i, j) == self.env.start_position:
                    R, G, B = 200, 20, 20
                elif (i, j) == self.env.goal_position:
                    R, G, B = 20, 200, 20
                elif (i, j) in self.env.obstacle_positions:
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

                if (i, j) == self.env.agent_position:
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
