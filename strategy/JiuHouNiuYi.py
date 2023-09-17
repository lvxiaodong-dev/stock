import pandas as pd
import talib


class JiuHouNiuYi:
    def __init__(self, name, df):
        self.name = name
        self.df = df

    def exec(self):
        df = self.df
        CLOSE = df['收盘']
        # HMA1为21日惠姆可编程移动平均线,色为黄色,线宽为1
        df.loc[:, 'HMA1'] = talib.WMA(2*talib.WMA(CLOSE,int(21/2)) - talib.WMA(CLOSE,21),int(21**0.5))

        # HMA2为88日惠姆可编程移动平均线,色为品红,线宽为2  
        df.loc[:, 'HMA2'] = talib.WMA(talib.WMA(CLOSE,int(21/2)) - talib.WMA(CLOSE,21),int(21**0.5))

        # B1判断收盘价是否低于4日前收盘价  
        df.loc[:, 'B1'] = CLOSE < CLOSE.shift(4)

        # NT0统计B1连续出现的天数
        df.loc[:, 'NT0'] = df['B1'].groupby((df['B1'] != df['B1'].shift()).cumsum()).cumsum()

        # TJ21判断NT0是否等于9
        df.loc[:, 'TJ21'] = df['NT0'] == 9

        # TJ23判断上一周期NT0是否在0-8之间
        df.loc[:, 'TJ23'] = df['NT0'].shift(1).between(0, 8)

        # AY1计算最后显示的数字
        # df['AY1'] = (df['TJ21'].shift(9) | df['TJ23'].shift(df['NT0'])).astype(int) * df['NT0']

        # 画出AY1数字
        #df.apply(lambda x: draw_number(x['AY1'],x['low'],x['AY1'],0,-15) if x['AY1'] > 0 and x['AY1'] < 9 else None, axis=1)

        # A1判断收盘价是否高于4日前收盘价
        df.loc[:, 'A1'] = CLOSE > CLOSE.shift(4)

        # NT统计A1连续出现的天数
        df.loc[:, 'NT'] = df['A1'].groupby((df['A1'] != df['A1'].shift()).cumsum()).cumsum()

        # BB判断触发条件
        N = 10
        df.loc[:, 'BB'] = (df['NT0'].shift(1)==9) & (df['NT0'].shift(1)>=1) & (df['NT0'].shift(1)<=N) & (df['NT']==1) & (CLOSE > CLOSE.shift(4))

        # 画出图标
        #df.apply(lambda x: draw_icon(x['BB'],x['low']*0.97,5) if x['BB'] else None,axis=1) 

        # 画出数字1
        #df.apply(lambda x: draw_number(x['BB'],x['high'],1,0,15) if x['BB'] else None,axis=1)
        if df['BB'].iat[-1]:
            return True
        return False
