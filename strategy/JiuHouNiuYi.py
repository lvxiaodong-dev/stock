import pandas as pd
import talib


class JiuHouNiuYi:
    def __init__(self, name, df):
        self.name = name
        self.df = df

    def exec(self):
        df = self.df
        # HMA1为21日惠姆可编程移动平均线,色为黄色,线宽为1
        today_close = df['收盘'].iat[-1]
        fourth_day_close = df['收盘'].iat[-5]
        yesterday_close = df['收盘'].iat[-2]
        fifth_day_close = df['收盘'].iat[-6]

        # 检查high_1条件
        if today_close > fourth_day_close and yesterday_close < fifth_day_close:
            high_1 = True
        else:
            high_1 = False

        # 检查low_9条件
        for k in range(1, 10):
            if df['收盘'].iat[-k] >= df['收盘'].iat[-k-4]:
                low_9 = False
                break

        # 检查在过去的13天内是否出现过 low_9
        if any(df['最低'][-14:] <= df['最低'].iat[-10]):
            low_9_appeared = True

        if high_1 and low_9_appeared:
            return True
        return False
