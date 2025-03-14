from main import Action, init_state, many_steps

if __name__ == "__main__":
    solution = [
        Action.PICK_GOAT,
        Action.CROSS_RIVER,
        Action.DROP_GOAT,
        Action.CROSS_RIVER,
        Action.PICK_WOLF,
        Action.CROSS_RIVER,
        Action.DROP_WOLF,
        Action.PICK_GOAT,
        Action.CROSS_RIVER,
        Action.DROP_GOAT,
        Action.PICK_CABBAGE,
        Action.CROSS_RIVER,
        Action.DROP_CABBAGE,
        Action.CROSS_RIVER,
        Action.PICK_GOAT,
        Action.CROSS_RIVER,
        Action.DROP_GOAT,
    ]

    final_state = many_steps(init_state, solution)
    print(final_state.solved())
