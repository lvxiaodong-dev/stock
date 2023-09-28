import pandas as pd
import talib


class Strategy:
    def __init__(self, name, recent_day):
        self.name = name
        self.recent_day = recent_day

    def set_df(self, df):
        self.df = df

    def exec(self):
        result = []
        for _ in range(self.recent_day):
            result.append(self.find())
            self.pop()
        return any(result)

    def pop(self):
        self.df = self.df.iloc[:-1]