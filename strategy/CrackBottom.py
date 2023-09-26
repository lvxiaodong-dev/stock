import numpy as np
from MyTT import EMA, REF, LLV, HHV, SMA, MAX, ABS, MA, MIN
from strategy.Strategy import Strategy
# 破底翻指标


class CrackBottom(Strategy):

    def __init__(self, *args):
        super().__init__(*args)

    def find(self):
        df = self.df
        CLOSE = df.CLOSE
        OPEN = df.OPEN
        LOW = df.LOW
        HIGH = df.HIGH
        VOL = df.VOL

        with np.errstate(invalid='ignore'):
            # 计算日线MACD
            N1 = 3
            N2 = 5
            N3 = 8
            N4 = 13

            # 1. MACD
            DIFF = EMA(CLOSE, N3) - EMA(CLOSE, N4)
            DEA = EMA(DIFF, N2)
            condition1 = DIFF[-1] > DEA[-1]

            # 2. KDJ
            RSV1 = (CLOSE - LLV(LOW, N3)) / (HHV(HIGH, N3) - LLV(LOW, N3)) * 100
            K = SMA(RSV1, N1, 1)
            D = SMA(K, N1, 1)
            condition2 = K[-1] > D[-1]

            # # 3. RSI
            LC = REF(CLOSE, 1)
            RSI1 = (SMA(MAX(CLOSE - LC, 0), N2, 1))/(SMA(ABS(CLOSE - LC), N2, 1)) * 100
            RSI2 = (SMA(MAX(CLOSE - LC, 0), N4, 1))/(SMA(ABS(CLOSE - LC), N4, 1)) * 100
            condition3 = RSI1[-1] > RSI2[-1]

            # 4. LWR
            RSV = -(HHV(HIGH, N4)-CLOSE)/(HHV(HIGH, N4)-LLV(LOW, N4))*100
            LWR1 = SMA(RSV, N1, 1)
            LWR2 = SMA(LWR1, N1, 1)
            condition4 = LWR1[-1] > LWR2[-1]

            # 5. BBI
            BBI = (MA(CLOSE, N1) + MA(CLOSE, N2) + MA(CLOSE, N3) + MA(CLOSE, N4)) / 4
            condition5 = CLOSE.iat[-1] > BBI[-1]

            # # # 6. MTM
            MTM = CLOSE - REF(CLOSE, 1)
            MMS = 100 * EMA(EMA(MTM, N2), N1) / EMA(EMA(ABS(MTM), N2), N1)
            MMM = 100 * EMA(EMA(MTM, N4), N3) / EMA(EMA(ABS(MTM), N4), N3)
            condition6 = MMS[-1] > MMM[-1]

            # 7. MMS
            WJ = (HIGH + LOW + CLOSE)/3
            V1= np.where(HIGH == LOW, 1, HIGH - MAX(0, CLOSE))
            V2= np.where(HIGH == LOW, 1, HIGH - MAX(CLOSE, 0) - WJ)
            V3= np.where(HIGH == LOW, 1, HIGH - MIN(0, CLOSE) - LOW)
            V4= np.where(HIGH == LOW, 1, HIGH - WJ - MIN(CLOSE, 0))
            V5 = VOL/np.where(HIGH == LOW, 4, HIGH - LOW)
            V6 = (V1*V5)
            V7 = (V2*V5)
            V8 = (V3*V5)
            V9 = (V4*V5)
            BUY_PRESSURE = (V9+V8)
            SELL_PRESSURE = (V6+V7)
            DIFF_PRESSURE = BUY_PRESSURE-SELL_PRESSURE
            DX = MA(DIFF_PRESSURE, 5)*20
            DDX1 = SMA(DX, 3, 1)
            DDX2 = SMA(DDX1, 3, 1)
            condition7 = DDX1[-1] > DDX2[-1]

            # 8. KDJ2
            RSV2 = (CLOSE-LLV(LOW, 40))/(HHV(HIGH, 40)-LLV(LOW, 40))*100
            K1 = SMA(RSV2, 18, 1)
            D1 = SMA(K1, 3, 1)
            J1 = 3*K1-2*D1
            K11 = J1 > REF(J1, 1)
            D11 = J1 < REF(J1, 1)
            condition8 = K11[-1] > D11[-1]

            # 9. TURNOVER RATE
            # TURNOVERRATE = VOL/CAPITAL*100
            # VAR1 = VOL/((HIGH-LOW)*2-ABS(CLOSE-OPEN))
            # BUY_PRESSURE1 = IF(CLOSE>OPEN,VAR1*(HIGH-LOW),IF(CLOSE<OPEN,VAR1*((HIGH-OPEN)+(CLOSE-LOW)),VOL/2))
            # SELL_PRESSURE1 = IF(CLOSE>OPEN,0-VAR1*((HIGH-CLOSE)+(OPEN-LOW)),IF(CLOSE<OPEN,0-VAR1*(HIGH-LOW),0-VOL/2))
            # DLX = (BUY_PRESSURE1-(-SELL_PRESSURE1))/VOL*TURNOVERRATE
            # DLX1 = SUM(DLX,6)
            # DLX2 = MA(DLX1,5);
            # condition8=DLX1>DLX2

            # # 判断买入条件
            if condition1 and condition2 and condition3 and condition4 and condition5 and condition6 and condition7 and condition8:
                return True
            return False

