from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    QUOTE = "quote"


@dataclass
class Order:
    order_id: int
    order_type: OrderType
    order_qty: int
    order_price: float
    order_time: int


# FillPrice could be unknown (None)
FillPrice = Optional[float]


def older_price(o1: Order, o2: Order) -> float:
    """Return the price of the older order."""
    return o2.order_price if o1.order_time > o2.order_time else o1.order_price


@dataclass
class OrderBook:
    buys: list[Order]
    sells: list[Order]

    def best_buy(self) -> Order | None:
        """Return the best buy order."""
        return self.buys[0] if self.buys else None

    def best_sell(self) -> Order | None:
        """Return the best sell order."""
        return self.sells[0] if self.sells else None

    def next_buy(self) -> Order | None:
        """Return the second-best buy order."""
        return self.buys[1] if len(self.buys) > 1 else None

    def next_sell(self) -> Order | None:
        """Return the second-best sell order."""
        return self.sells[1] if len(self.sells) > 1 else None


def get_next_best_price(ob: OrderBook, is_buy: bool) -> float | None:
    """Get the next best price for buy or sell."""
    next_order = ob.next_buy() if is_buy else ob.next_sell()
    return (
        next_order.order_price
        if next_order and next_order.order_type != OrderType.MARKET
        else None
    )


def determine_fill_price(
    b_bid: float | None, b_ask: float | None, ref_price: float
) -> float:
    """Determine the fill price based on next best orders and reference price."""
    if b_bid is None and b_ask is None:
        return ref_price
    elif b_bid is None and b_ask is not None:
        return b_ask if b_ask < ref_price else ref_price
    elif b_bid is not None and b_ask is None:
        return b_bid if b_bid > ref_price else ref_price
    else:
        return b_bid if b_bid > ref_price else b_ask if b_ask < ref_price else ref_price


def match_price(ob: OrderBook, ref_price: float) -> FillPrice:
    """Determine the fill price for matching orders in the order book."""
    bb: Order | None = ob.best_buy()
    bs: Order | None = ob.best_sell()
    if bb is None or bs is None:
        return None

    bb_type, bs_type = bb.order_type, bs.order_type

    if (bb_type == OrderType.LIMIT and bs_type == OrderType.LIMIT) or (
        bb_type == OrderType.QUOTE and bs_type == OrderType.QUOTE
    ):
        return older_price(bb, bs)
    elif bb_type == OrderType.MARKET and bs_type == OrderType.MARKET:
        if bb.order_qty != bs.order_qty:
            return None
        else:
            b_bid = get_next_best_price(ob, True)
            b_ask = get_next_best_price(ob, False)
            return determine_fill_price(b_bid, b_ask, ref_price)
    elif bb_type == OrderType.MARKET and bs_type == OrderType.LIMIT:
        return bs.order_price
    elif bb_type == OrderType.LIMIT and bs_type == OrderType.MARKET:
        return bb.order_price
    elif bb_type == OrderType.QUOTE and bs_type == OrderType.LIMIT:
        if bb.order_time > bs.order_time:
            if bb.order_qty < bs.order_qty:
                return bs.order_price
            elif bb.order_qty == bs.order_qty:
                next_sell = ob.next_sell()
                return next_sell.order_price if next_sell else bb.order_price
            else:
                return None
        else:
            return bb.order_price
    elif bb_type == OrderType.QUOTE and bs_type == OrderType.MARKET:
        if bb.order_time > bs.order_time:
            next_sell_limit = ob.next_sell()
            if bb.order_qty < bs.order_qty:
                return bs.order_price
            elif bb.order_qty == bs.order_qty:
                return (
                    next_sell_limit.order_price if next_sell_limit else bb.order_price
                )
            else:
                return None
        else:
            return bb.order_price
    elif bb_type == OrderType.LIMIT and bs_type == OrderType.QUOTE:
        if bb.order_time > bs.order_time:
            if bs.order_qty < bb.order_qty:
                return bb.order_price
            elif bs.order_qty == bb.order_qty:
                next_buy = ob.next_buy()
                return next_buy.order_price if next_buy else bs.order_price
            else:
                return None
        else:
            return bs.order_price
    elif bb_type == OrderType.MARKET and bs_type == OrderType.QUOTE:
        if bb.order_time > bs.order_time:
            if bs.order_qty < bb.order_qty:
                return bs.order_price
            elif bb.order_qty == bs.order_qty:
                next_buy_limit = ob.next_buy()
                return next_buy_limit.order_price if next_buy_limit else bs.order_price
            else:
                return None
        else:
            return bs.order_price
    else:
        return None
