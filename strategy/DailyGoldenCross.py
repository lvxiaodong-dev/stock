import pandas as pd
import talib as ta
from strategy.Strategy import Strategy

class DailyGoldenCross(Strategy):
  def __init__(self, *args):
    super().__init__(*args)

  def find(self):
    CLOSE = self.CLOSE()

    # 计算日线MACD
    macd_diff, macd_dea, macd_bar = ta.MACD(CLOSE, fastperiod=12, slowperiod=26, signalperiod=9) 
    macd_diff = macd_diff.dropna()
    macd_dea = macd_dea.dropna()

    # 判断金叉
    if macd_diff.iat[-1] > macd_dea.iat[-1] and macd_diff.iat[-2] < macd_dea.iat[-2]:
      return True
    return False
  