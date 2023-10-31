import pandas as pd
import talib as ta
from MyTT import MA
from strategy.Strategy import Strategy

# 周线金叉


class DailyMA(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            CLOSE = df.CLOSE

            ma5 = MA(CLOSE, 5)
            ma10 = MA(CLOSE, 10)
            ma20 = MA(CLOSE, 20)
            ma30 = MA(CLOSE, 30)

            # 5 10 20 30均线多头排列
            condition1 = ma5[-1] > ma10[-1] and ma10[-1] > ma20[-1] and ma20[-1] > ma30[-1]
            condition2 = ~(ma5[-2] > ma10[-2] and ma10[-2] > ma20[-2] and ma20[-2] > ma30[-2])

            if condition1 and condition2:
                return True

        except IndexError:
            return False
        return False
