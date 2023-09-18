import pandas as pd
import talib
import numpy as np
from MyTT import REF,MAX,ABS,SMA,MA,CROSS
from strategy.Strategy import Strategy

class LiuCaiShenLong(Strategy):
    def __init__(self, name, df, dynamic_day):
        super().__init__(name, df, dynamic_day)

    def find(self):
        df = self.df
        CLOSE = df['收盘']

        N = self.dynamic_day

        MM_BASE = 50;
        MM_PERIOD = 50;
        MM_SENS = 1.5;

        LC = REF(CLOSE,1);
        TEMP1 = MAX(CLOSE-LC,0);
        TEMP2 = ABS(CLOSE-LC);
        with np.errstate(invalid='ignore'):
            RSI1 = SMA(TEMP1,MM_PERIOD,1)/SMA(TEMP2,MM_PERIOD,1)*100;
            RSI_B = MM_SENS*(RSI1-MM_BASE);
            MM_RSI = False

            # 满足最近出现N个红柱子
            condition1 = np.all(RSI_B[-N:] > 0)
            condition2 = RSI_B[-N-1] < 0
            # MM_RSI = min(max(RSI_B[-1], 0), 20)
            MM_RSI = np.where(RSI_B > 20, 20, np.where(RSI_B < 0, 0, RSI_B))
            ZLX = MA(MM_RSI*5,10);
            condition3 = CROSS(MM_RSI, ZLX)[-1]

            
            # # 判断买入条件
            if condition1 and condition2 and condition3:
                return True
            return False