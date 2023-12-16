import talib as ta
from strategy.Strategy import Strategy
from MyTT import LAST, BARSLAST

class MACDRedDot(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            CLOSE = df.CLOSE

            macd_diff, macd_dea, macd_bar = ta.MACD(
                CLOSE, fastperiod=12, slowperiod=26, signalperiod=9)
            macd_diff = macd_diff.dropna()
            macd_dea = macd_dea.dropna()

            绿柱=macd_bar>0
            红柱=macd_bar<0
            持续天数=5
            绿柱持续=LAST(绿柱,持续天数,1)
            绿丛中红=绿柱持续 & 红柱
            绿丛中红至今天数=BARSLAST(绿丛中红)
            F=绿丛中红至今天数==1
            绿丛中一点红=F & 绿柱
            if 绿丛中一点红.iloc[-2]:
                return True
            return False
        except IndexError:
            return False
