import pandas as pd
from MyTT import EMA, REF, FORCAST, BARSLAST
from strategy.Strategy import Strategy

class HongLiBeiLiWang(Strategy):
  def __init__(self, name, df, dynamic_day):
    super().__init__(name, df, dynamic_day)

  def find(self):
    # 向量化计算指标
    CLOSE = self.CLOSE()
    A1 = FORCAST(EMA(CLOSE, 5), 6)
    A2 = FORCAST(EMA(CLOSE, 8), 6)
    A3 = FORCAST(EMA(CLOSE, 11), 6)
    A4 = FORCAST(EMA(CLOSE, 14), 6)
    A5 = FORCAST(EMA(CLOSE, 17), 6)
    B = A1+A2+A3+A4-4*A5
    TOWERC = EMA(B, 2)
    
    FLAG = TOWERC >= REF(TOWERC, 1)
    FLAG1 = pd.Series(REF(FLAG, 1)).bfill()
    COND1 = FLAG & (~FLAG1)
    PERIOD_COND1 = BARSLAST(REF(COND1,1));
    COND2 = (CLOSE.iat[-1] < REF(CLOSE, PERIOD_COND1[-1] + 1)[-1]) & (TOWERC[-1] > REF(TOWERC, PERIOD_COND1[-1] + 1)[-1])
    
    # 记录结果
    if COND1.iat[-1] & COND2:
        return True
    return False
  