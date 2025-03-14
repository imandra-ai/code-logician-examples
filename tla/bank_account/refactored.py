from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce


@dataclass
class BankState:
    alice_account: int = 10
    bob_account: int = 10
    money: int = 5


class Actions:
    @staticmethod
    def withdraw_from_alice(state: BankState) -> BankState:
        """Withdraw money from Alice's account"""
        return BankState(
            alice_account=state.alice_account - state.money,
            bob_account=state.bob_account,
            money=state.money,
        )

    @staticmethod
    def deposit_to_bob(state: BankState) -> BankState:
        """Deposit money into Bob's account"""
        return BankState(
            alice_account=state.alice_account,
            bob_account=state.bob_account + state.money,
            money=state.money,
        )


class Transfers:
    @staticmethod
    def transfer(state: BankState) -> BankState:
        """Perform a transfer from Alice to Bob"""
        return reduce(
            lambda s, f: f(s),
            [Actions.withdraw_from_alice, Actions.deposit_to_bob],
            state,
        )

    @staticmethod
    def safe_transfer(state: BankState) -> BankState:
        """Perform a transfer only if Alice has sufficient funds"""
        transfer_chain: list[Callable[[BankState], BankState]] = [
            Actions.deposit_to_bob
        ]
        if state.alice_account >= state.money:
            transfer_chain.insert(0, Actions.withdraw_from_alice)
        return reduce(lambda s, f: f(s), transfer_chain, state)


init_account: dict[str, int] = {
    "alice_account": 10,
    "bob_account": 10,
}

# Verify that for any positive transfer amount, Alice's account balance remains non-negative after a regular transfer with the initial account balances

# Verify that for any positive transfer amount, Alice's account balance remains non-negative after a safe transfer with the initial account balances
