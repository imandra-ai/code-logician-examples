from dataclasses import dataclass
from enum import Enum, auto


class MarketCondition(Enum):
    NORMAL = auto()
    CROSSED = auto()
    LOCKED = auto()


class OrderSide(Enum):
    BUY = auto()
    SELL = auto()
    SELL_SHORT = auto()


class OrderPeg(Enum):
    NEAR = auto()
    MID = auto()
    FAR = auto()
    NO_PEG = auto()


class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()
    PEGGED = auto()
    PEGGED_CI = auto()
    LIMIT_CI = auto()
    FIRM_UP_PEGGED = auto()
    FIRM_UP_LIMIT = auto()

    @property
    def is_ci(self) -> bool:
        """Check if order type is a Conditional Indication (CI)"""
        return self in (OrderType.PEGGED_CI, OrderType.LIMIT_CI)

    @property
    def is_limit_type(self) -> bool:
        """Check if order type is a limit-based type"""
        return self in (OrderType.LIMIT, OrderType.LIMIT_CI, OrderType.FIRM_UP_LIMIT)

    @property
    def is_pegged_type(self) -> bool:
        """Check if order type is a pegged-based type"""
        return self in (OrderType.PEGGED, OrderType.PEGGED_CI, OrderType.FIRM_UP_PEGGED)


@dataclass
class MarketData:
    nbb: float  # National best bid
    nbo: float  # National best offer
    l_up: float
    l_down: float

    @property
    def mid_point(self) -> float:
        """Calculate the midpoint of the NBBO"""
        return (self.nbb + self.nbo) / 2.0

    def valid_market_data(self) -> bool:
        """Check if market data is valid"""
        return (
            self.l_down > 0.0
            and self.nbb > self.l_down
            and self.nbo > self.nbb
            and self.l_up > self.nbo
        )


@dataclass
class Order:
    id: int
    peg: OrderPeg
    client_id: int
    order_type: OrderType
    qty: int
    min_qty: int
    leaves_qty: int
    price: float
    time: int

    def valid_order(self) -> bool:
        """Check if order is valid"""
        return (
            self.leaves_qty <= self.qty
            and self.time >= 0
            and self.price > 0.0
            and self.qty > 0
            and self.leaves_qty >= 0
        )


def less_aggressive(side: OrderSide, lim_price: float, far_price: float) -> float:
    if lim_price < 0.0:
        return far_price
    elif side == OrderSide.BUY:
        return min(lim_price, far_price)
    else:
        return max(lim_price, far_price)


def priority_price(side: OrderSide, o: Order, mkt: MarketData) -> float:
    if o.order_type in [OrderType.LIMIT, OrderType.LIMIT_CI, OrderType.FIRM_UP_LIMIT]:
        # Calculate NBBO capped limit
        if side == OrderSide.BUY:
            return less_aggressive(OrderSide.BUY, o.price, mkt.nbo)
        else:
            return less_aggressive(OrderSide.SELL, o.price, mkt.nbb)
    elif o.order_type == OrderType.MARKET:
        return mkt.nbo if side == OrderSide.BUY else mkt.nbb
    else:  # PEGGED, PEGGED_CI, FIRM_UP_PEGGED
        # Calculate pegged price
        if o.peg == OrderPeg.FAR:
            return less_aggressive(
                side, o.price, mkt.nbo if side == OrderSide.BUY else mkt.nbb
            )
        elif o.peg == OrderPeg.MID:
            return less_aggressive(side, o.price, mkt.mid_point())
        elif o.peg == OrderPeg.NEAR:
            return less_aggressive(
                side, o.price, mkt.nbb if side == OrderSide.BUY else mkt.nbo
            )
        else:  # NO_PEG
            return o.price


def order_higher_ranked(
    side: OrderSide, o1: Order, o2: Order, market: MarketData
) -> bool:
    p_price1 = priority_price(side, o1, market)
    p_price2 = priority_price(side, o2, market)

    # Determine if o1 wins on price
    if side == OrderSide.BUY:
        price_comparison = p_price1 - p_price2
    else:  # SELL or SELL_SHORT
        price_comparison = p_price2 - p_price1

    # If prices are different, higher price (for buy) or lower price (for sell) wins
    if price_comparison > 0:
        return True
    elif price_comparison < 0:
        return False

    # Same price level - apply additional rules
    # If both are CI orders, larger quantity wins
    if o1.order_type.is_ci and o2.order_type.is_ci:
        return o1.leaves_qty > o2.leaves_qty

    # Time priority
    if o1.time != o2.time:
        return o1.time < o2.time

    # Non-CI orders have priority over CI orders
    if not o1.order_type.is_ci and o2.order_type.is_ci:
        return True
    elif o1.order_type.is_ci and not o2.order_type.is_ci:
        return False

    # If we get here, compare by quantity for CI orders
    return o1.leaves_qty > o2.leaves_qty


def rank_transitivity(
    side: OrderSide, o1: Order, o2: Order, o3: Order, market: MarketData
) -> bool:
    """
    Check if ranking is transitive: if o1 > o2 and o2 > o3, then o1 > o3
    """
    if order_higher_ranked(side, o1, o2, market) and order_higher_ranked(
        side, o2, o3, market
    ):
        return order_higher_ranked(side, o1, o3, market)
    return True


# Check that then rank transitivity holds

# Check that if orders and market data are valid, then rank transitivity holds
