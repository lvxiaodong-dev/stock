import pandas as pd
import talib


class Strategy:
    def __init__(self, name, dynamic_day):
        self.name = name
        self.dynamic_day = dynamic_day

    def set_df(self, df):
        self.df = df

    def exec(self):
        result = []
        for _ in range(self.dynamic_day):
            result.append(self.find())
            self.pop()
        return any(result)

    def pop(self):
        self.df = self.df.iloc[:-1]

    def OPEN(self):
        return self.df['开盘'] if '开盘' in self.df.columns else self.df['Open']
    
    def CLOSE(self):
        return self.df['收盘'] if '收盘' in self.df.columns else self.df['Close']
    
    def HIGH(self):
        return self.df['最高'] if '最高' in self.df.columns else self.df['High']
    
    def LOW(self):
        return self.df['最低'] if '最低' in self.df.columns else self.df['Low']