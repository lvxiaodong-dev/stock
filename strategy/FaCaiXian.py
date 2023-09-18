import pandas as pd
import talib
import math
from strategy.Strategy import Strategy

class FaCaiXian(Strategy):
    def __init__(self, name, df, dynamic_day):
        super().__init__(name, df, dynamic_day)

    def find(self):
        df = self.df
        CLOSE = self.CLOSE()

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
        return False
  