from dataclasses import dataclass


@dataclass
class BankState:
    alice_account: int = 10
    bob_account: int = 10
    money: int = 5


class Actions:
    @staticmethod
    def withdraw_from_alice(state):
        """Withdraw money from Alice's account"""
        return BankState(
            alice_account=state.alice_account - state.money,
            bob_account=state.bob_account,
            money=state.money,
        )

    @staticmethod
    def deposit_to_bob(state):
        """Deposit money into Bob's account"""
        return BankState(
            alice_account=state.alice_account,
            bob_account=state.bob_account + state.money,
            money=state.money,
        )


def transfer(state):
    """Perform a transfer from Alice to Bob"""
    state = Actions.withdraw_from_alice(state)
    state = Actions.deposit_to_bob(state)
    return state


def safe_transfer(state):
    """Perform a transfer only if Alice has sufficient funds"""
    if state.alice_account < state.money:
        return state
    else:
        state = Actions.withdraw_from_alice(state)
        state = Actions.deposit_to_bob(state)


init_account = {
    "alice_account": 10,
    "bob_account": 10,
}

# Verify that for any positive transfer amount, Alice's account balance remains non-negative after a regular transfer with the initial account balances

# Verify that for any positive transfer amount, Alice's account balance remains non-negative after a safe transfer with the initial account balances
