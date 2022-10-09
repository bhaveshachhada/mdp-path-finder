from collections import defaultdict

import constants
from environment import Environment


class MDPSolver:

    def __init__(self, environment: Environment):
        self.env = environment


class PolicyIterationSolver(MDPSolver):

    def __init__(self, environment: Environment):
        MDPSolver.__init__(self, environment)
        self._converged = False

        self._policy = None
        self._state_space = self.env.get_all_states()
        self._start_state = self.env.get_start_state()
        self._state_value = None
        self._state_transition_probability = None

    def initialise(self):
        self._policy = defaultdict(lambda: constants.Move.FORWARD)
        self._state_value = defaultdict(lambda: 0.0)
        self._calculate_state_transition_probability()

    def iterate(self):
        self.evaluate()
        self.improvise()

    def evaluate(self): ...

    def improvise(self): ...

    @property
    def converged(self) -> bool:
        return self._converged

    def _calculate_state_transition_probability(self):
        self._state_transition_probability = dict()
        for state in self._state_space:
            self._state_transition_probability[state] = dict()
            for action in constants.Move:
                self._state_transition_probability[state][action] = defaultdict(lambda: 0.0)
                _, new_state = self.env.apply_dynamics(state, action)
                self._state_transition_probability[state][action][new_state] = 1.0
