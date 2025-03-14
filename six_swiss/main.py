from dataclasses import dataclass
from enum import Enum


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
FillPrice = float | None


def older_price(o1: Order, o2: Order) -> float:
    if o1.order_time > o2.order_time:
        return o2.order_price
    else:
        return o1.order_price


@dataclass
class OrderBook:
    buys: list[Order]
    sells: list[Order]

    def best_buy(self) -> Order | None:
        if self.buys:
            return self.buys[0]
        else:
            return None

    def best_sell(self) -> Order | None:
        if self.sells:
            return self.sells[0]
        else:
            return None

    def next_buy(self) -> Order | None:
        """Second-best buy order of the book"""
        if len(self.buys) < 2:
            return None
        else:
            return self.buys[1]

    def next_sell(self) -> Order | None:
        """Second-best sell order"""
        if len(self.sells) < 2:
            return None
        else:
            return self.sells[1]


def match_price(ob: OrderBook, ref_price: float) -> FillPrice:
    """Determine the fill price for matching orders in the order book.

    Args:
        ob: The order book containing buy and sell orders
        ref_price: Reference price of the exchange. This refers to the last stable fill
            price that the exchange traded on. Acts as an 'anchor' price when the order
            book lacks sufficient information to determine a fill price.

    Returns:
        The fill price if orders can be matched, None otherwise
    """
    bb: Order | None = ob.best_buy()
    bs: Order | None = ob.best_sell()
    # If there are no buy or sell orders, return None
    if bb is None or bs is None:
        return None

    bb_type, bs_type = bb.order_type, bs.order_type

    # When matching Limit/Limit or Quote/Quote orders, the fill price is simply the
    # older order's price
    if (bb_type == OrderType.LIMIT and bs_type == OrderType.LIMIT) or (
        bb_type == OrderType.QUOTE and bs_type == OrderType.QUOTE
    ):
        return older_price(bb, bs)
    elif bb_type == OrderType.MARKET and bs_type == OrderType.MARKET:
        if bb.order_qty != bs.order_qty:
            return None
        else:
            # Need to look at other orders in the order book
            # Get the next best order's price if it exists and is not a market order
            b_bid: float | None = None
            next_buy = ob.next_buy()
            if next_buy and next_buy.order_type != OrderType.MARKET:
                b_bid = next_buy.order_price

            b_ask: float | None = None
            next_sell = ob.next_sell()
            if next_sell and next_sell.order_type != OrderType.MARKET:
                b_ask = next_sell.order_price

            # Determine fill price based on next best orders and reference price
            if b_bid is None and b_ask is None:
                return ref_price
            elif b_bid is None and b_ask is not None:
                return b_ask if b_ask < ref_price else ref_price
            elif b_bid is not None and b_ask is None:
                return b_bid if b_bid > ref_price else ref_price
            else:
                if b_bid > ref_price:
                    return b_bid
                elif b_ask < ref_price:
                    return b_ask
                else:
                    return ref_price

    elif bb_type == OrderType.MARKET and bs_type == OrderType.LIMIT:
        return bs.order_price
    elif bb_type == OrderType.LIMIT and bs_type == OrderType.MARKET:
        return bb.order_price

    elif bb_type == OrderType.QUOTE and bs_type == OrderType.LIMIT:
        if bb.order_time > bs.order_time:
            # incoming quote
            if bb.order_qty < bs.order_qty:
                return bs.order_price
            elif bb.order_qty == bs.order_qty:
                next_sell = ob.next_sell()
                if next_sell:
                    return next_sell.order_price
                else:
                    return bb.order_price
            else:
                return None
        else:
            # existing quote's price is used
            return bb.order_price

    elif bb_type == OrderType.QUOTE and bs_type == OrderType.MARKET:
        if bb.order_time > bs.order_time:
            # incoming quote
            next_sell_limit = ob.next_sell()
            if bb.order_qty < bs.order_qty:
                return bs.order_price
            elif bb.order_qty == bs.order_qty:
                if next_sell_limit:
                    return next_sell_limit.order_price
                else:
                    return bb.order_price
            else:
                return None
        else:
            # The quote's price is used
            return bb.order_price

    elif bb_type == OrderType.LIMIT and bs_type == OrderType.QUOTE:
        if bb.order_time > bs.order_time:
            # incoming quote
            if bs.order_qty < bb.order_qty:
                return bb.order_price
            elif bs.order_qty == bb.order_qty:
                next_buy = ob.next_buy()
                if next_buy:
                    return next_buy.order_price
                else:
                    return bs.order_price
            else:
                return None
        else:
            # existing quote's price is used
            return bs.order_price

    elif bb_type == OrderType.MARKET and bs_type == OrderType.QUOTE:
        if bb.order_time > bs.order_time:
            # incoming quote
            if bs.order_qty < bb.order_qty:
                return bs.order_price
            elif bb.order_qty == bs.order_qty:
                next_buy_limit = ob.next_buy()
                if next_buy_limit:
                    return next_buy_limit.order_price
                else:
                    return bs.order_price
            else:
                return None
        else:
            # The quote's price is used
            return bs.order_price

    else:
        return None
