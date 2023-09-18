import sys
from strategy.Strategy import Strategy
sys.path.append('../libs')
from MyTT import REF,LLV,HHV,LLV,SMA,AVEDEV,MA
from libs.zig import ZIG
from libs.troughbars import TROUGHBARS


class HeiMa(Strategy):
    def __init__(self, name, df, dynamic_day):
        super().__init__(name, df, dynamic_day)

    def find(self):
        # 向量化计算指标
        df = self.df
        OPEN = df['Open'] if self.us else df['开盘']
        CLOSE = df['Close'] if self.us else df['收盘']
        HIGH = df['High'] if self.us else df['最高']
        LOW = df['Low'] if self.us else df['最低']

        N = 9
        M1 = 3
        M2 = 3
        VAR1 = (HIGH+LOW+CLOSE)/3
        VAR2 = (VAR1-MA(VAR1, 14))/(0.015*AVEDEV(VAR1, 14))
        VAR3 = False
        z = ZIG(df, 3, 22)
        VAR3 = 1 if TROUGHBARS(
            df, 3, 0.16, 1)[-2] == 1 and (HIGH.iat[-1] > LOW.iat[-1]+0.04) else 0
        VAR4 = 1 if (z[-1] > z[-2] and z[-2] <=
                     z[-3] and z[-3] <= z[-4]) else 0
        if VAR2.iat[-2] < -110 and VAR3 == 1 and VAR4 == 1:
            return True
        return False
    