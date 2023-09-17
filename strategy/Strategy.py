import pandas as pd
import talib


class Strategy:
    def __init__(self, name, df):
        self.name = name
        self.df = df

    def pop(self):
        self.df = self.df.iloc[:-1]