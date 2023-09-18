import pandas as pd
import talib as ta
from strategy.Strategy import Strategy

class DailyGoldenCross(Strategy):
  def __init__(self, name, df, dynamic_day):
    super().__init__(name, df, dynamic_day)

  def find(self):
    # 计算日线MACD
    macd_diff, macd_dea, macd_bar = ta.MACD(self.df['收盘'], fastperiod=12, slowperiod=26, signalperiod=9) 
    macd_diff = macd_diff.dropna()
    macd_dea = macd_dea.dropna()

    # 判断金叉
    if macd_diff.iat[-1] > macd_dea.iat[-1] and macd_diff.iat[-2] < macd_dea.iat[-2]:
      return True
    return False
  