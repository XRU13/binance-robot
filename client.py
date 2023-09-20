import decimal
import time
from typing import List

from config import client
from dataclasses import Order, OrderBook, Density


class BinanceAPI:

    def get_all_pair(self, symbol: str) -> List[str]:
        tickers = client.get_all_tickers()
        pairs = [ticker['symbol'] for ticker in tickers if symbol in ticker['symbol']]

        return pairs

    def get_order_book(self, symbol: str, limit: int = 100) -> OrderBook:
        order_book = client.get_order_book(symbol=symbol, limit=limit)

        bids = [Order(decimal.Decimal(price), decimal.Decimal(quantity)) for price, quantity, *_ in order_book['bids']]
        asks = [Order(decimal.Decimal(price), decimal.Decimal(quantity)) for price, quantity, *_ in order_book['asks']]
        return OrderBook(asks=asks, bids=bids)

    def get_greatest_buy_sell_amount(self, order_book: OrderBook) -> Density:
        bids_book = order_book.bids
        asks_book = order_book.asks

        max_bids_amount = max([order.quantity for order in bids_book])
        greatest_buy_order = {}
        for bid in bids_book:
            if bid.quantity == max_bids_amount:
                greatest_buy_order = bid

        max_asks_amount = max([order.quantity for order in asks_book])
        greatest_sell_order = {}
        for ask in asks_book:
            if ask.quantity == max_asks_amount:
                greatest_sell_order = ask

        return Density(
            dense_axis_bid=greatest_buy_order,
            dense_axis_ask=greatest_sell_order
        )

    def get_max_trading_volume(self, symbol: str, interval: str, time_range: int) -> float:
        end_time = int(time.time() * 1000)
        start_time = end_time - time_range * 60 * 1000
        klines = client.get_klines(symbol=symbol, interval=interval, startTime=start_time, endTime=end_time)
        max_volume = max(float(kline[5]) for kline in klines)

        return max_volume

    def get_price_step(self, symbol: str) -> float:
        symbol_info = client.get_symbol_info(symbol=symbol)
        filters = symbol_info['filters']
        price_step = 0
        for api_filter in filters:
            if api_filter['filterType'] == 'PRICE_FILTER':
                return float(api_filter['tickSize'])
