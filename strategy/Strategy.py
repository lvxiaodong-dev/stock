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

    def pop(self):
        self.df = self.df.iloc[:-1]