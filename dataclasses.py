import decimal
from typing import List

from attr import dataclass


@dataclass
class Order:
    price: decimal.Decimal
    quantity: decimal.Decimal


@dataclass
class OrderBook:
    bids: List[Order]
    asks: List[Order]


@dataclass
class Density:
    dense_axis_bid: Order
    dense_axis_ask: Order
