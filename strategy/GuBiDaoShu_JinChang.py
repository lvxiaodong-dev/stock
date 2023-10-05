import math
import pandas as pd
import talib as ta
import numpy as np
from MyTT import BARSLAST, REF, LLV, CONST, HHV, IF
from strategy.Strategy import Strategy

# 日线金叉


class GuBiDaoShu_JinChang(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        df = self.df
        # 向量化计算指标
        CLOSE = df.CLOSE
        HIGH = df.HIGH
        LOW = df.LOW

        P = 21
        CURRBARSCOUNT = list(range(len(HIGH), 0, -1))

        # WH1
        WH1 = IF(LOW == LLV(LOW, P), LOW, None)
        # WH2
        WH2 = CONST(BARSLAST(WH1 != None))
        # WH3
        WH3 = CONST(IF(WH2 == 0, HIGH, REF(HIGH, WH2[-1])))
        # WH4
        WH4 = CONST(REF(BARSLAST(HIGH > WH3), WH2[-1]+1)+WH2[-1]+1)
        # WH5
        WH5 = CONST(IF(WH4 == 0, HIGH, REF(HIGH, int(WH4[-1]))))
        # WH6
        WH6 = CONST(REF(BARSLAST(HIGH > WH5), int(WH4[-1])+1)+int(WH4[-1])+1)
        # 进场
        entry_circle_dot = IF(
            CURRBARSCOUNT <= WH2+21, CONST(IF(WH6 == 0, HIGH, REF(HIGH, int(WH6[-1])))), None)
        if CLOSE.iat[-2] <= entry_circle_dot[-1] and CLOSE.iat[-1] > entry_circle_dot[-1]:
            return True
        return False
