import copy
from typing import List, Optional

from client import BinanceAPI
from constants import TimeRange, EXCLUDED_PAIR
from config import client
from dataclasses import Order


class BinanceTrade:
    # Минимальное расстояние между плотностями
    MIN_DISTANCE = 5

    def __init__(self):
        self.binance_api = BinanceAPI()
        self.verification_coefficient = 2

    def check_density(self):
        all_pairs = self.binance_api.get_all_pair(symbol='USDT')

        for pair in all_pairs[9:]:
            if pair in EXCLUDED_PAIR:
                continue

            # Получение всех заявок в стакане (глубина запроса 100)
            book = self.binance_api.get_order_book(symbol=pair)
            if not book:
                continue

            # Максимальный объем за 5 минут на основе последних 30 минут
            max_trading_volume = self.binance_api.get_max_trading_volume(
                symbol=pair,
                interval=client.KLINE_INTERVAL_5MINUTE,
                time_range=TimeRange.RANGE_30_MINUTE
            )

            # Получение максимальной плотности в стакане
            # greatest_density = self.binance_api.get_greatest_buy_sell_amount(
            #     order_book=book)

            # Получение плотностей в стакане
            asks_data = []
            bids_data = []
            asks_book = book.asks
            bids_book = book.bids
            coefficient = max_trading_volume * self.verification_coefficient

            for book in asks_book:
                if book.quantity > coefficient:
                    asks_data.append(book)

            for book in bids_book:
                if book.quantity > coefficient:
                    bids_data.append(book)

            # Получение минимального шага цены по паре
            price_step = self.binance_api.get_price_step(symbol=pair)

            if len(asks_data) > 1:
                ask_density = self.check_density_location_and_size(
                    densities=asks_data, price_step=price_step)
                if not ask_density:
                    print('Нет плотностей')

            # Если плотность в стакане одна
            elif len(asks_data) == 1:
                f = 5
            else:
                print('Нет плотностей')

            if len(bids_data) > 1:
                bid_density = self.check_density_location_and_size(
                    densities=bids_data, price_step=price_step)
            elif len(bids_data) == 1:
                d = 9
            else:
                print('Нет плотностей')

            s = 0

        # if greatest_density.dense_axis_ask.quantity > max_trading_volume * 25:
        #     print(
        #         f'For pair: {pair} dense ask: '
        #         f'{greatest_density.dense_axis_ask} - max value: {max_trading_volume}'
        #     )
        # if greatest_density.dense_axis_bid.quantity >= max_trading_volume * 20:
        #     print(
        #         f'For pair: {pair} dense bid: '
        #         f'{greatest_density.dense_axis_bid} - max value: {max_trading_volume}'
        #     )

    def check_density_location_and_size(
        self,
        densities: List[Order],
        price_step: float,
    ) -> Optional[Order]:
        copy_densities = copy.deepcopy(densities)

        for density in range(len(densities) - 1):

            # Если плотностей больше чем одна,
            # сравниваем их удаленность друг от друга
            if len(densities) > 1:
                first_density = densities[0].price
                second_density = densities[1].price

                min_distance = price_step * self.MIN_DISTANCE
                difference_step = abs(first_density - second_density)

                # Если расстояние между ними меньше MIN_DISTANCE,
                # то удаляем обе
                if difference_step < min_distance:
                    densities.pop(0)
                    densities.pop(0)
                    continue

                # Если больше, проверяем на размер относительно друг друга
                else:
                    first_density_quantity = densities[0].quantity
                    second_density_quantity = densities[1].quantity

                    # Если первая плотность больше чем вдвое второй,
                    # то удаляем вторую плотность
                    if first_density_quantity > second_density_quantity * 2:
                        densities.pop(1)

                    # Если вторая плотность больше чем вдвое первая,
                    # то удаляем первую плотность
                    elif second_density_quantity > first_density_quantity * 2:
                        densities.pop(0)

                    # Иначе удаляем обе
                    else:
                        densities.pop(0)
                        densities.pop(0)

            # Возвращаем одну плотность, либо None если плотностей не осталось
            else:
                return densities[0] if densities else None

    def test_movement(self):
        pass


if __name__ == '__main__':
    print(BinanceTrade().check_density())
