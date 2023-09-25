import pandas as pd
import talib
import numpy as np
from MyTT import REF,MAX,ABS,SMA,MA,CROSS
from strategy.Strategy import Strategy

class LiuCaiShenLongGreen(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        df = self.df
        CLOSE = self.CLOSE()

        N = 3

        MM_BASE = 50;
        MM_PERIOD = 50;
        MM_SENS = 1.5;

        HOT_BASE = 30;
        HOT_PERIOD = 40;
        HOT_SENS = 0.7;

        LC = REF(CLOSE,1);
        TEMP1 = MAX(CLOSE-LC,0);
        TEMP2 = ABS(CLOSE-LC);
        with np.errstate(invalid='ignore'):
            RSI1 = SMA(TEMP1,MM_PERIOD,1)/SMA(TEMP2,MM_PERIOD,1)*100;
            RSI_B = MM_SENS*(RSI1-MM_BASE);

            RSI2 = SMA(TEMP1,HOT_PERIOD,1)/SMA(TEMP2,HOT_PERIOD,1)*100;
            RSI_M = HOT_SENS*(RSI2-HOT_BASE);

            condition1 = (RSI_B[-1] + RSI_M[-1]) * 5 <= 20

            # # 判断买入条件
            if condition1:
                return True
            return False