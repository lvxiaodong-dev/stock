from MyTT import REF, LLV, HHV, LLV, SMA, AVEDEV, MA
from libs.troughbars import TROUGHBARS
from libs.zig import ZIG
import sys
from strategy.Strategy import Strategy
sys.path.append('../libs')

# 黑马


class HeiMa(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def exec(self, **kwargs):
        return self.find(**kwargs)

    def find(self, df, info):
        try:
            day = self.recent_day
            # 向量化计算指标
            OPEN = df.OPEN
            CLOSE = df.CLOSE
            HIGH = df.HIGH
            LOW = df.LOW

            VAR1 = (HIGH+LOW+CLOSE)/3
            VAR2 = (VAR1-MA(VAR1, 14))/(0.015*AVEDEV(VAR1, 14))

            for index in range(day):
                VAR3 = False
                z = ZIG(df, 3, 22)
                VAR3 = 1 if TROUGHBARS(
                    df, 3, 0.16, 1)[-2-index] == 1 and (HIGH.iat[-1-index] > LOW.iat[-1-index]+0.04) else 0
                VAR4 = 1 if (z[-1-index] > z[-2-index] and z[-2-index]
                             <= z[-3-index] and z[-3-index] <= z[-4-index]) else 0
                if VAR2.iat[-2-index] < -110 and VAR3 == 1 and VAR4 == 1:
                    return True
        except IndexError:
            return False
        return False
