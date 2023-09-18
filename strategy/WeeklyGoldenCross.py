import pandas as pd
import talib as ta
from strategy.Strategy import Strategy

class WeeklyGoldenCross(Strategy):
  def __init__(self, name, df, dynamic_day):
    super().__init__(name, df, dynamic_day)

  def find(self):
    CLOSE = self.CLOSE()

    # 计算周线MACD 
    wk_macd_diff, wk_macd_dea, wk_macd_bar = ta.MACD(CLOSE, fastperiod=26, slowperiod=52, signalperiod=13)
    wk_macd_diff = wk_macd_diff.dropna()
    wk_macd_dea = wk_macd_dea.dropna()

    # 判断金叉
    if wk_macd_diff.iat[-1] > wk_macd_dea.iat[-1] and wk_macd_diff.iat[-2] < wk_macd_dea.iat[-2]:
      return True
    return False