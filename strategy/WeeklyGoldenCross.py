import pandas as pd
import talib as ta

class WeeklyGoldenCross:
  def __init__(self, name, df):
    self.name = name
    self.df = df

  def exec(self):
    # 计算周线MACD 
    wk_macd_diff, wk_macd_dea, wk_macd_bar = ta.MACD(self.df['收盘'], fastperiod=26, slowperiod=52, signalperiod=13)
    wk_macd_diff = wk_macd_diff.dropna()
    wk_macd_dea = wk_macd_dea.dropna()

    # 判断金叉
    if wk_macd_diff.iat[-1] < wk_macd_dea.iat[-1] and wk_macd_diff.iat[-2] > wk_macd_dea.iat[-2]:
      return True
    return False