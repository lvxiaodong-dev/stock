import pandas as pd
import talib
import math
from strategy.Strategy import Strategy

# 发财线


class FaCaiXian(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        try:
            df = self.df
            CLOSE = df.CLOSE

            N = 88
            # 最近10天都在发财线之下
            S = slice(-10, -1)

            # 计算发财线
            mid = talib.WMA(CLOSE, 44)
            wma = talib.WMA(CLOSE, N)
            temp = 2*mid - wma
            hma = talib.WMA(temp, int(math.sqrt(N)))

            # 判断金叉
            if all(hma[S] > CLOSE[S]) and hma.iat[-1] < CLOSE.iat[-1]:
                return True
        except IndexError:
            return False
