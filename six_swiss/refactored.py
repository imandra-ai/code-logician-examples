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


def match_limit_or_quote_orders(bb: Order, bs: Order) -> FillPrice:
    if (bb.order_type == OrderType.LIMIT and bs.order_type == OrderType.LIMIT) or (
        bb.order_type == OrderType.QUOTE and bs.order_type == OrderType.QUOTE
    ):
        return older_price(bb, bs)
    return None


def get_next_non_market_price(order: Order | None) -> float | None:
    if order and order.order_type != OrderType.MARKET:
        return order.order_price
    return None


def determine_market_market_price(
    bb: Order, bs: Order, ob: OrderBook, ref_price: float
) -> FillPrice:
    if bb.order_qty != bs.order_qty:
        return None

    b_bid = get_next_non_market_price(ob.next_buy())
    b_ask = get_next_non_market_price(ob.next_sell())

    if b_bid is None and b_ask is None:
        return ref_price
    elif b_bid is None:
        return b_ask if b_ask < ref_price else ref_price
    elif b_ask is None:
        return b_bid if b_bid > ref_price else ref_price
    else:
        if b_bid > ref_price:
            return b_bid
        elif b_ask < ref_price:
            return b_ask
        else:
            return ref_price


def match_market_limit_orders(bb: Order, bs: Order) -> FillPrice:
    if bb.order_type == OrderType.MARKET and bs.order_type == OrderType.LIMIT:
        return bs.order_price
    elif bb.order_type == OrderType.LIMIT and bs.order_type == OrderType.MARKET:
        return bb.order_price
    return None


def handle_quote_limit_match(
    quote: Order, limit: Order, ob: OrderBook, is_buy_quote: bool
) -> FillPrice:
    if quote.order_time > limit.order_time:
        if quote.order_qty < limit.order_qty:
            return limit.order_price
        elif quote.order_qty == limit.order_qty:
            next_order = ob.next_sell() if is_buy_quote else ob.next_buy()
            return next_order.order_price if next_order else quote.order_price
        else:
            return None
    return quote.order_price if is_buy_quote else limit.order_price


def match_quote_limit_orders(bb: Order, bs: Order, ob: OrderBook) -> FillPrice:
    if bb.order_type == OrderType.QUOTE and bs.order_type == OrderType.LIMIT:
        return handle_quote_limit_match(bb, bs, ob, True)
    elif bb.order_type == OrderType.LIMIT and bs.order_type == OrderType.QUOTE:
        return handle_quote_limit_match(bs, bb, ob, False)
    return None


def match_quote_market_orders(bb: Order, bs: Order, ob: OrderBook) -> FillPrice:
    if bb.order_type == OrderType.QUOTE and bs.order_type == OrderType.MARKET:
        return handle_quote_limit_match(bb, bs, ob, True)
    elif bb.order_type == OrderType.MARKET and bs.order_type == OrderType.QUOTE:
        return handle_quote_limit_match(bs, bb, ob, False)
    return None


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

    if bb is None or bs is None:
        return None

    return (
        match_limit_or_quote_orders(bb, bs)
        or (
            determine_market_market_price(bb, bs, ob, ref_price)
            if bb.order_type == OrderType.MARKET and bs.order_type == OrderType.MARKET
            else None
        )
        or match_market_limit_orders(bb, bs)
        or match_quote_limit_orders(bb, bs, ob)
        or match_quote_market_orders(bb, bs, ob)
    )
