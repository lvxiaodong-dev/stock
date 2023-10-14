import pandas as pd
import talib as ta
from strategy.Strategy import Strategy
from MyTT import MAX, ABS, REF, EMA, SMA, MA, LLV, HHV, CROSS

# 建仓信号


class QueKouJiuZhuan_JianCang(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        try:
            df = self.df
            CLOSE = df.CLOSE
            OPEN = df.OPEN
            LOW = df.LOW
            HIGH = df.HIGH

            VAR1 = LLV(LOW, 21)
            VAR2 = HHV(HIGH, 21)
            AK1 = EMA((((CLOSE - VAR1) / (VAR2 - VAR1)) * 100), 5)
            AK = EMA((((CLOSE - VAR1) / (VAR2 - VAR1)) * 50), 13)
            AB = CROSS(AK1, AK)

            # 判断金叉
            if AB[-1]:
                return True
        except IndexError:
            return False
        return False
