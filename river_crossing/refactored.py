from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce


class Location(Enum):
    BOAT = auto()
    LEFT_COAST = auto()
    RIGHT_COAST = auto()
    EATEN = auto()


class Boat(Enum):
    LEFT = auto()
    RIGHT = auto()


class Good(Enum):
    CABBAGE = auto()
    GOAT = auto()
    WOLF = auto()


@dataclass(frozen=True)
class State:
    cabbage: Location = Location.LEFT_COAST
    goat: Location = Location.LEFT_COAST
    wolf: Location = Location.LEFT_COAST
    boat: Boat = Boat.LEFT

    def copy(self) -> "State":
        """Create a deep copy of the state"""
        return State(
            cabbage=self.cabbage,
            goat=self.goat,
            wolf=self.wolf,
            boat=self.boat,
        )

    def get_location(self, good: Good) -> Location:
        """Get the location of a specific good"""
        return {Good.CABBAGE: self.cabbage, Good.GOAT: self.goat, Good.WOLF: self.wolf}[
            good
        ]

    def set_location(self, good: Good, location: Location) -> "State":
        """Create a new state with the specified good at the given location"""
        return State(
            cabbage=location if good == Good.CABBAGE else self.cabbage,
            goat=location if good == Good.GOAT else self.goat,
            wolf=location if good == Good.WOLF else self.wolf,
            boat=self.boat,
        )

    def pick(self, good: Good) -> "State":
        """Pick up an item and put it in the boat if possible"""
        if not self.boat_empty():
            return self

        good_location = self.get_location(good)
        can_pick = (
            good_location == Location.LEFT_COAST and self.boat == Boat.LEFT
        ) or (good_location == Location.RIGHT_COAST and self.boat == Boat.RIGHT)

        return self.set_location(good, Location.BOAT) if can_pick else self

    def drop(self, good: Good) -> "State":
        """Drop an item from the boat to the coast"""
        good_location = self.get_location(good)
        if good_location != Location.BOAT:
            return self

        new_location = (
            Location.LEFT_COAST if self.boat == Boat.LEFT else Location.RIGHT_COAST
        )
        return self.set_location(good, new_location)

    def boat_empty(self) -> bool:
        """Check if the boat is empty"""
        return all(self.get_location(good) != Location.BOAT for good in Good)

    def solved(self) -> bool:
        """Check if the puzzle is solved"""
        return all(self.get_location(good) == Location.RIGHT_COAST for good in Good)

    def process_eating(self) -> "State":
        """Check if any item gets eaten and return the resulting state"""

        def check_eating_condition(state: State) -> tuple[Good, Location] | None:
            conditions = [
                (
                    state.boat == Boat.RIGHT
                    and state.cabbage == Location.LEFT_COAST
                    and state.goat == Location.LEFT_COAST,
                    Good.CABBAGE,
                ),
                (
                    state.boat == Boat.RIGHT
                    and state.goat == Location.LEFT_COAST
                    and state.wolf == Location.LEFT_COAST,
                    Good.GOAT,
                ),
                (
                    state.boat == Boat.LEFT
                    and state.cabbage == Location.RIGHT_COAST
                    and state.goat == Location.RIGHT_COAST,
                    Good.CABBAGE,
                ),
                (
                    state.boat == Boat.LEFT
                    and state.goat == Location.RIGHT_COAST
                    and state.wolf == Location.RIGHT_COAST,
                    Good.GOAT,
                ),
            ]
            return next(
                ((good, Location.EATEN) for condition, good in conditions if condition),
                None,
            )

        eating_result = check_eating_condition(self)
        return (
            self.set_location(eating_result[0], eating_result[1])
            if eating_result
            else self
        )

    def anything_eaten(self) -> bool:
        """Check if cabbage or goat has been eaten"""
        return any(
            self.get_location(good) == Location.EATEN
            for good in [Good.CABBAGE, Good.GOAT]
        )

    def __repr__(self) -> str:
        def format_side(items: list[str]) -> str:
            return "".join(sorted(items))

        def get_position_str(good: Good) -> tuple[str, str, str]:
            location = self.get_location(good)
            symbol = good.name[0]
            left = symbol if location == Location.LEFT_COAST else ""
            right = symbol if location == Location.RIGHT_COAST else ""
            boat = symbol if location == Location.BOAT else ""
            return left, boat, right

        left_items, boat_items, right_items = zip(
            *(get_position_str(good) for good in Good), strict=False
        )

        boat_str = "B" if not boat_items else next(item for item in boat_items if item)
        river = f"...{boat_str}" if self.boat == Boat.RIGHT else f"{boat_str}..."

        return f"{format_side(left_items):>3} |{river}| {format_side(right_items):<3}"


class Action(Enum):
    CROSS_RIVER = auto()
    PICK_CABBAGE = auto()
    PICK_GOAT = auto()
    PICK_WOLF = auto()
    DROP_CABBAGE = auto()
    DROP_GOAT = auto()
    DROP_WOLF = auto()


def apply_action(state: State, action: Action) -> State:
    """Apply an action to a state"""
    actions = {
        Action.CROSS_RIVER: lambda s: State(
            cabbage=s.cabbage,
            goat=s.goat,
            wolf=s.wolf,
            boat=Boat.RIGHT if s.boat == Boat.LEFT else Boat.LEFT,
        ),
        Action.PICK_CABBAGE: lambda s: s.pick(Good.CABBAGE),
        Action.PICK_GOAT: lambda s: s.pick(Good.GOAT),
        Action.PICK_WOLF: lambda s: s.pick(Good.WOLF),
        Action.DROP_CABBAGE: lambda s: s.drop(Good.CABBAGE),
        Action.DROP_GOAT: lambda s: s.drop(Good.GOAT),
        Action.DROP_WOLF: lambda s: s.drop(Good.WOLF),
    }
    return actions.get(action, lambda s: s)(state)


def one_step(state: State, action: Action) -> State:
    """Process one step of the game given a state and an action"""
    if state.anything_eaten():
        return state
    return apply_action(state, action).process_eating()


def many_steps(state: State, actions: Sequence[Action]) -> State:
    """Process multiple steps of the game"""

    def step_reducer(current_state: State, action: Action) -> State:
        return (
            current_state
            if current_state.anything_eaten()
            else one_step(current_state, action)
        )

    return reduce(step_reducer, actions, state)


init_state = State(
    cabbage=Location.LEFT_COAST,
    goat=Location.LEFT_COAST,
    wolf=Location.LEFT_COAST,
    boat=Boat.LEFT,
)
