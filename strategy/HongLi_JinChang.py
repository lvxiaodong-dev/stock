import pandas as pd
import talib as ta
from MyTT import EMA, CROSS
from strategy.Strategy import Strategy

# 弘历进场

class HongLi_JinChang(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            CLOSE = df.CLOSE
            hpos1 = EMA(CLOSE, 8)
            hpos2 = EMA(CLOSE, 20)
            condition1 = CROSS(hpos1, hpos2)
            if condition1[-1]:
                return True
        except IndexError:
            return False
        return False
