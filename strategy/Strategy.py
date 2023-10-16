import pandas as pd
import talib

# 父类
class Strategy:
    def __init__(self, name, recent_day):
        self.name = name
        self.recent_day = recent_day

    def exec(self, **kwargs):
        result = []
        for _ in range(self.recent_day):
            result.append(self.find(**kwargs))
            kwargs['df'] = self.pop(kwargs['df'])
        return any(result)

    def pop(self, df):
        df = df.iloc[:-1]
        return df