import pandas as pd
import talib as ta
from MyTT import EMA, CROSS, MAX, MIN
from strategy.Strategy import Strategy

# 乾坤线进场2


class QianKunXian2(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            CLOSE = df.CLOSE
            SHORT = 12
            LONG = 26
            M = 9

            DIF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
            DEA = EMA(DIF, M)
            MACD = (DIF - DEA) * 2

            if MACD[-1] > 0 and MACD[-2] < 0 and MACD[-3] < 0 and MACD[-4] < 0 and MACD[-5] < 0 and MACD[-6] < 0 and MACD[-7] < 0 and MACD[-8] < 0 and MACD[-9] < 0 and MACD[-10] < 0 and MACD[-11] < 0 and MACD[-12] < 0 and MACD[-13] < 0 and MACD[-14] < 0 and MACD[-15] < 0 and MACD[-16] < 0 and MACD[-17] < 0 and MACD[-18] < 0 and MACD[-19] < 0 and MACD[-20] < 0 and MACD[-21] < 0 and MACD[-22] < 0 and MACD[-23] < 0:
                return True
        except IndexError:
            return False
        return False
