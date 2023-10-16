import pandas as pd
import numpy as np
from MyTT import EMA, REF, FORCAST, BARSLAST
from strategy.Strategy import Strategy

# 弘历背离王


class HongLiBeiLiWang(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            # 向量化计算指标
            CLOSE = df.CLOSE
            A1 = FORCAST(EMA(CLOSE, 5), 6)
            A2 = FORCAST(EMA(CLOSE, 8), 6)
            A3 = FORCAST(EMA(CLOSE, 11), 6)
            A4 = FORCAST(EMA(CLOSE, 14), 6)
            A5 = FORCAST(EMA(CLOSE, 17), 6)
            B = A1+A2+A3+A4-4*A5
            TOWERC = EMA(B, 2)

            FLAG = TOWERC >= REF(TOWERC, 1)
            FLAG1 = REF(FLAG, 1)
            COND1 = np.logical_and(FLAG, FLAG1)
            PERIOD_COND1 = BARSLAST(REF(COND1, 1))
            COND2 = (CLOSE.iat[-1] < REF(CLOSE, PERIOD_COND1[-1] + 1)[-1]
                     ) & (TOWERC[-1] > REF(TOWERC, PERIOD_COND1[-1] + 1)[-1])

            # 记录结果
            if COND1[-1] & COND2:
                return True
        except IndexError:
            return False
        return False
