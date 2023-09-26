import pandas as pd
import talib as ta
from MyTT import EMA, REF, FORCAST, BARSLAST
from strategy.Strategy import Strategy

# 破底翻指标

class CrackBottom(Strategy):
  def __init__(self, *args):
    super().__init__(*args)

  def find(self):
    CLOSE = self.CLOSE()
    # 计算日线MACD
    N1=3;N2=5;N3=8;N4=13;

    
    DIFF=EMA(CLOSE,6{N3})-EMA(CLOSE,13{N4});
    DEA=EMA(DIFF,4{N2});
    DRAWTEXT((DIFF>DEA),1,'●'),COLORBLUE,LINETHICK1;
    DRAWTEXT((DIFF<DEA),1,'●'),COLORRED,LINETHICK1;
    A1:=DIFF>DEA

    # 判断金叉
    if macd_diff.iat[-1] > macd_dea.iat[-1] and macd_diff.iat[-2] < macd_dea.iat[-2]:
      return True
    return False
  