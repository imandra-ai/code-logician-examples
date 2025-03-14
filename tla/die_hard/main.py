from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class State:
    """Represents the state of the two jugs."""

    big: int = 0  # Water in the 5-gallon jug
    small: int = 0  # Water in the 3-gallon jug

    @staticmethod
    def init_state() -> "State":
        """Initial state of the problem."""
        return State()

    def solved(self) -> bool:
        """Checks if the state is a solution."""
        return self.big == 4


class Action(Enum):
    """Enumeration of possible actions"""

    FILL_SMALL = auto()
    FILL_BIG = auto()
    EMPTY_SMALL = auto()
    EMPTY_BIG = auto()
    SMALL_TO_BIG = auto()
    BIG_TO_SMALL = auto()


def apply(action: Action, state: State) -> State:
    """Apply this action to the given state, returning a new state."""
    if action == Action.FILL_SMALL:
        return State(state.big, 3)
    elif action == Action.FILL_BIG:
        return State(5, state.small)
    elif action == Action.EMPTY_SMALL:
        return State(state.big, 0)
    elif action == Action.EMPTY_BIG:
        return State(0, state.small)
    elif action == Action.SMALL_TO_BIG:
        # Calculate how much water will be in the big jug
        new_big = min(state.big + state.small, 5)
        # Small jug loses exactly what big jug gains
        new_small = state.small - (new_big - state.big)
        return State(new_big, new_small)
    elif action == Action.BIG_TO_SMALL:
        # Calculate how much water will be in the small jug
        new_small = min(state.big + state.small, 3)
        # Big jug loses exactly what small jug gains
        new_big = state.big - (new_small - state.small)
        return State(new_big, new_small)


def many_steps(state: State, actions: list[Action]) -> State:
    """Apply a list of actions to a state, returning the final state."""
    for action in actions:
        state = apply(action, state)
    return state


# Find a solution that starts from the initial state and ends with the solution state


# Prove that there is no solution with less than 3 steps
