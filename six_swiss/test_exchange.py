from main import Order, OrderBook, OrderType, match_price


class TestMatchPrice:
    def setUp(self):
        self.order1 = Order(1, OrderType.LIMIT, 100, 12.56, 1)
        self.order2 = Order(2, OrderType.LIMIT, 100, 12.56, 2)
        self.order3 = Order(3, OrderType.LIMIT, 100, 40.0, 3)

    def test_basic_limit_orders(self):
        # Test case 1: Basic matching of limit orders
        self.setUp()
        ob = OrderBook(buys=[self.order1], sells=[self.order2])
        ref_price = 123.45
        assert match_price(ob, ref_price) == 12.56

    def test_multiple_sell_orders(self):
        # Test case 2: Multiple sell orders
        self.setUp()
        ob = OrderBook(buys=[self.order1], sells=[self.order2, self.order3])
        ref_price = 123.45
        assert match_price(ob, ref_price) == 12.56

    def test_consistency(self):
        # Test case 3: Same orders as previous test to verify consistency
        self.setUp()
        ob = OrderBook(buys=[self.order1], sells=[self.order2, self.order3])
        ref_price = 123.45
        assert match_price(ob, ref_price) == 12.56

    def test_higher_priced_buy(self):
        # Test case 4: Higher priced buy order
        self.setUp()
        ob = OrderBook(buys=[self.order3], sells=[self.order1, self.order2])
        ref_price = 34.44
        assert match_price(ob, ref_price) == 12.56


if __name__ == "__main__":
    test = TestMatchPrice()
    test.test_basic_limit_orders()
    test.test_multiple_sell_orders()
    test.test_consistency()
    test.test_higher_priced_buy()
    print("All tests passed!")
