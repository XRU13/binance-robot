from enum import Enum

EXCLUDED_PAIR = ['BTCUSDT', 'ETHUSDT', 'ARUSDT', 'SKLUSDT', 'KAVAUSDT']


class Limit(int, Enum):
    SEARCH_DEPTH_100 = 100
    SEARCH_DEPTH_200 = 200
    SEARCH_DEPTH_300 = 300
    SEARCH_DEPTH_400 = 400
    SEARCH_DEPTH_500 = 500
    SEARCH_DEPTH_600 = 600
    SEARCH_DEPTH_700 = 700
    SEARCH_DEPTH_800 = 800
    SEARCH_DEPTH_900 = 900
    SEARCH_DEPTH_1000 = 1000


class TimeRange(int, Enum):
    RANGE_5_MINUTE = 5
    RANGE_10_MINUTE = 10
    RANGE_15_MINUTE = 15
    RANGE_30_MINUTE = 30
    RANGE_45_MINUTE = 45
    RANGE_60_MINUTE = 60
