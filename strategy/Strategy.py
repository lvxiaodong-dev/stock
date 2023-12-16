import pandas as pd
import numpy as np

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

    def findSell(self, df, info):
        print(f"WARNING: no sell stragtegy for {self.name}")
        return False

    def execSell(self, **kwargs):
        result = []
        for _ in range(self.recent_day):
            result.append(self.findSell(**kwargs))
            kwargs['df'] = self.pop(kwargs['df'])
        return any(result)

    def transactions(self, df, info):
        print(f"WARNING: no backTestfor {self.name}")
        arr = np.full(df.size, False)
        return arr, arr

    def YahooDf(self, df):
        return df.rename(columns={'OPEN': 'Open', 'CLOSE':'Close', 'HIGH' : 'High', 'LOW': 'Low', 'VOL':'Volume'})