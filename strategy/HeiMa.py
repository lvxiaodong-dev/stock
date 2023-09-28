import sys
from strategy.Strategy import Strategy
sys.path.append('../libs')
from MyTT import REF,LLV,HHV,LLV,SMA,AVEDEV,MA
from libs.zig import ZIG
from libs.troughbars import TROUGHBARS


class HeiMa(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def exec(self):
        return self.find()

    def find(self):
        df = self.df
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
            z = ZIG(self, 3, 22)
            VAR3 = 1 if TROUGHBARS(self, 3, 0.16, 1)[-2-index] == 1 and (HIGH.iat[-1-index] > LOW.iat[-1-index]+0.04) else 0
            VAR4 = 1 if (z[-1-index] > z[-2-index] and z[-2-index] <= z[-3-index] and z[-3-index] <= z[-4-index]) else 0
            if VAR2.iat[-2-index] < -110 and VAR3 == 1 and VAR4 == 1:
                return True
            
        return False
    