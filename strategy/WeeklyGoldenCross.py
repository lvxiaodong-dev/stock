import pandas as pd
import talib as ta
from strategy.Strategy import Strategy

# 周线金叉


class WeeklyGoldenCross(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            CLOSE = df.CLOSE

            # 计算周线MACD
            macd_diff, macd_dea, macd_bar = ta.MACD(
                CLOSE, fastperiod=26, slowperiod=52, signalperiod=13)
            macd_diff = macd_diff.dropna()
            macd_dea = macd_dea.dropna()

            # 判断金叉
            if macd_diff.iat[-1] > macd_dea.iat[-1] and macd_diff.iat[-2] < macd_dea.iat[-2]:
                return True
        except IndexError:
            return False
        return False
