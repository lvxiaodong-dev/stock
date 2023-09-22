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
        return self.df['open']
    
    def CLOSE(self):
        return self.df['close']
    
    def HIGH(self):
        return self.df['high']
    
    def LOW(self):
        return self.df['low']