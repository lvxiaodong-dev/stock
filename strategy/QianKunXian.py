import pandas as pd
import talib as ta
from MyTT import EMA, CROSS, MAX, MIN
from strategy.Strategy import Strategy

# 日线金叉
class QianKunXian(Strategy):
  def __init__(self, *args):
    super().__init__(*args)

  def find(self):
    df = self.df
    CLOSE = df.CLOSE
    SHORT = 12
    LONG = 26
    M = 9

    DIF = EMA(CLOSE, SHORT) - EMA(CLOSE, LONG)
    DEA = EMA(DIF, M)

    # 零轴之下金叉
    if CROSS(DIF, DEA)[-1] and MAX(DIF, DEA)[-1] <= 0:
      return True
    # 零轴之上金叉
    if CROSS(DIF, DEA)[-1] and MIN(DIF, 0)[-1] <= 0:
      return True
    
    return False
  