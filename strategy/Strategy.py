import pandas as pd
import talib


class Strategy:
    def __init__(self, name, df, dynamic_day):
        self.name = name
        self.df = df
        self.dynamic_day = dynamic_day

    def exec(self):
        result = []
        for _ in range(self.dynamic_day):
            result.append(self.find())
            self.pop()
        return any(result)
        self.us = True if 'Open' in df.columns else False

    def pop(self):
        self.df = self.df.iloc[:-1]

    def OPEN(self):
        return self.df['Open'] if self.us else self.df['开盘']
    
    def CLOSE(self):
        return self.df['Close'] if self.us else self.df['收盘']
    
    def HIGH(self):
        return self.df['High'] if self.us else self.df['最高']
    
    def LOW(self):
        return self.df['Low'] if self.us else self.df['最低']