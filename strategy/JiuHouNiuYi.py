import pandas as pd
from strategy.Strategy import Strategy

# 九后牛一
class JiuHouNiuYi(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        df = self.df
        CLOSE = df.CLOSE

        # B1判断收盘价是否低于4日前收盘价  
        df.loc[:, 'B1'] = CLOSE < CLOSE.shift(4)

        # NT0统计B1连续出现的天数
        df.loc[:, 'NT0'] = df['B1'].groupby((df['B1'] != df['B1'].shift()).cumsum()).cumsum()

        # A1判断收盘价是否高于4日前收盘价
        df.loc[:, 'A1'] = CLOSE > CLOSE.shift(4)

        # NT统计A1连续出现的天数
        df.loc[:, 'NT'] = df['A1'].groupby((df['A1'] != df['A1'].shift()).cumsum()).cumsum()

        # BB判断触发条件
        N = 10
        df.loc[:, 'BB'] = (df['NT0'].shift(1)==9) & (df['NT0'].shift(1)>=1) & (df['NT0'].shift(1)<=N) & (df['NT']==1) & (CLOSE > CLOSE.shift(4))

        if df['BB'].iat[-1]:
            return True
        return False
