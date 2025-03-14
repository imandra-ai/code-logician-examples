"""
Die Hard Water Jug Problem

This module models the famous water jug problem from Die Hard 3, where the
heroes must obtain exactly 4 gallons of water using a 5-gallon jug, a 3-gallon jug,
and a water faucet.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce


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

    def transfer(
        capacity: int, source_amount: int, target_amount: int
    ) -> tuple[int, int]:
        new_target = min(source_amount + target_amount, capacity)
        new_source = source_amount - (new_target - target_amount)
        return new_target, new_source

    def handle_small_to_big(s: State) -> State:
        new_big, new_small = transfer(5, s.small, s.big)
        return State(new_big, new_small)

    def handle_big_to_small(s: State) -> State:
        new_small, new_big = transfer(3, s.big, s.small)
        return State(new_big, new_small)

    actions: dict[Action, Callable[[State], State]] = {
        Action.FILL_SMALL: lambda s: State(s.big, 3),
        Action.FILL_BIG: lambda s: State(5, s.small),
        Action.EMPTY_SMALL: lambda s: State(s.big, 0),
        Action.EMPTY_BIG: lambda s: State(0, s.small),
        Action.SMALL_TO_BIG: handle_small_to_big,
        Action.BIG_TO_SMALL: handle_big_to_small,
    }

    return actions[action](state)


def many_steps(state: State, actions: list[Action]) -> State:
    """Apply a list of actions to a state, returning the final state."""
    return reduce(lambda s, a: apply(a, s), actions, state)


# Find a solution that starts from the initial state and ends with the solution state


# Prove that there is no solution with less than 3 steps
