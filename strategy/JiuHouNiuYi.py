import pandas as pd
from strategy.Strategy import Strategy

# 九后牛一
class JiuHouNiuYi(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        try:
            df = self.df
            CLOSE = df.CLOSE

            # B1判断收盘价是否低于4日前收盘价
            B1 = CLOSE < CLOSE.shift(4)

            # NT0统计B1连续出现的天数
            NT0 = B1.groupby((B1 != B1.shift()).cumsum()).cumsum()

            # A1判断收盘价是否高于4日前收盘价
            A1 = CLOSE > CLOSE.shift(4)

            # NT统计A1连续出现的天数
            NT = A1.groupby((A1 != A1.shift()).cumsum()).cumsum()

            # BB判断触发条件
            N = 10
            BB = (NT0.shift(1) == 9) & (NT0.shift(1) >= 1) & (
                NT0.shift(1) <= N) & (NT == 1) & (CLOSE > CLOSE.shift(4))

            if BB.iat[-1]:
                return True
        except IndexError:
            return False
        return False
