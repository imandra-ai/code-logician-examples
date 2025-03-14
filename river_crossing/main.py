from dataclasses import dataclass
from enum import Enum, auto


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


@dataclass
class State:
    cabbage: Location = Location.LEFT_COAST
    goat: Location = Location.LEFT_COAST
    wolf: Location = Location.LEFT_COAST
    boat: Boat = Boat.LEFT

    def copy(self):
        """Create a deep copy of the state"""
        return State(
            cabbage=self.cabbage,
            goat=self.goat,
            wolf=self.wolf,
            boat=self.boat,
        )

    def get_location(self, good):
        """Get the location of a specific good"""
        if good == Good.CABBAGE:
            return self.cabbage
        elif good == Good.GOAT:
            return self.goat
        elif good == Good.WOLF:
            return self.wolf

    def set_location(self, good, location):
        """Create a new state with the specified good at the given location"""
        if good == Good.CABBAGE:
            self.cabbage = location
        elif good == Good.GOAT:
            self.goat = location
        elif good == Good.WOLF:
            self.wolf = location

    def pick(self, good):
        """Pick up an item and put it in the boat if possible"""
        if not self.boat_empty():
            return

        good_location = self.get_location(good)

        if (good_location == Location.LEFT_COAST and self.boat == Boat.LEFT) or (
            good_location == Location.RIGHT_COAST and self.boat == Boat.RIGHT
        ):
            self.set_location(good, Location.BOAT)

    def drop(self, good):
        """Drop an item from the boat to the coast"""
        good_location = self.get_location(good)

        if good_location == Location.BOAT:
            if self.boat == Boat.LEFT:
                self.set_location(good, Location.LEFT_COAST)
            else:
                self.set_location(good, Location.RIGHT_COAST)

    def boat_empty(self):
        """Check if the boat is empty"""
        return (
            self.cabbage != Location.BOAT
            and self.goat != Location.BOAT
            and self.wolf != Location.BOAT
        )

    def solved(self):
        """Check if the puzzle is solved"""
        return (
            self.cabbage == Location.RIGHT_COAST
            and self.goat == Location.RIGHT_COAST
            and self.wolf == Location.RIGHT_COAST
        )

    def process_eating(self):
        """Check if any item gets eaten and return the resulting state"""
        if (
            self.boat == Boat.RIGHT
            and self.cabbage == Location.LEFT_COAST
            and self.goat == Location.LEFT_COAST
        ):
            self.cabbage = Location.EATEN
        elif (
            self.boat == Boat.RIGHT
            and self.goat == Location.LEFT_COAST
            and self.wolf == Location.LEFT_COAST
        ):
            self.goat = Location.EATEN
        elif (
            self.boat == Boat.LEFT
            and self.cabbage == Location.RIGHT_COAST
            and self.goat == Location.RIGHT_COAST
        ):
            self.cabbage = Location.EATEN
        elif (
            self.boat == Boat.LEFT
            and self.goat == Location.RIGHT_COAST
            and self.wolf == Location.RIGHT_COAST
        ):
            self.goat = Location.EATEN

    def anything_eaten(self):
        """Check if cabbage or goat has been eaten"""
        return self.cabbage == Location.EATEN or self.goat == Location.EATEN

    def __repr__(self):
        left, right = "", ""
        if self.boat == Boat.LEFT:
            river = "B..."
        else:
            river = "...B"
        if self.cabbage == Location.LEFT_COAST:
            left += "C"
        elif self.cabbage == Location.RIGHT_COAST:
            right += "C"
        elif self.cabbage == Location.BOAT:
            river = river.replace("B", "C")
        if self.goat == Location.LEFT_COAST:
            left += "G"
        elif self.goat == Location.RIGHT_COAST:
            right += "G"
        elif self.goat == Location.BOAT:
            river = river.replace("B", "G")
        if self.wolf == Location.LEFT_COAST:
            left += "W"
        elif self.wolf == Location.RIGHT_COAST:
            right += "W"
        elif self.wolf == Location.BOAT:
            river = river.replace("B", "W")
        return f"{left:>3} |{river}| {right:<3}"


class Action(Enum):
    CROSS_RIVER = auto()
    PICK_CABBAGE = auto()
    PICK_GOAT = auto()
    PICK_WOLF = auto()
    DROP_CABBAGE = auto()
    DROP_GOAT = auto()
    DROP_WOLF = auto()


def apply_action(state, action):
    """Apply an action to a state"""
    if action == Action.CROSS_RIVER:
        state.boat = Boat.RIGHT if state.boat == Boat.LEFT else Boat.LEFT
    elif action == Action.PICK_CABBAGE:
        state.pick(Good.CABBAGE)
    elif action == Action.PICK_GOAT:
        state.pick(Good.GOAT)
    elif action == Action.PICK_WOLF:
        state.pick(Good.WOLF)
    elif action == Action.DROP_CABBAGE:
        state.drop(Good.CABBAGE)
    elif action == Action.DROP_GOAT:
        state.drop(Good.GOAT)
    elif action == Action.DROP_WOLF:
        state.drop(Good.WOLF)
    else:
        raise ValueError(f"Invalid action: {action}")


def one_step(state, action):
    """
    Process one step of the game given a state and an action function

    Args:
        state: The current game state
        action: The action to apply

    Returns:
        The new state after applying the action and checking for eating
    """
    # If anything has been eaten, stop the game
    if state.anything_eaten():
        return state

    new_state = state.copy()

    # Apply the action
    apply_action(new_state, action)

    # Check if anything has been eaten
    new_state.process_eating()

    return new_state


def many_steps(state, actions):
    """
    Process multiple steps of the game

    Args:
        state: The initial game state
        actions: A list of actions to apply in sequence

    Returns:
        The final state after applying all actions
    """
    current_state = state
    for action in actions:
        current_state = one_step(current_state, action)
        if current_state.anything_eaten():
            return current_state
    return current_state


init_state = State(
    cabbage=Location.LEFT_COAST,
    goat=Location.LEFT_COAST,
    wolf=Location.LEFT_COAST,
    boat=Boat.LEFT,
)
