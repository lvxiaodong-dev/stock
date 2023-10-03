import numpy as np
from MyTT import EMA, REF, LLV, HHV, SMA, MAX, ABS, MA, MIN
from strategy.Strategy import Strategy
from libs.findlowbars import FINDLOWBARS

# 破底翻指标
class CrackBottom(Strategy):

    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        df = self.df
        CLOSE = df.CLOSE
        OPEN = df.OPEN
        LOW = df.LOW
        HIGH = df.HIGH
        VOL = df.VOL

        return False

