from strategy.Strategy import Strategy
from MyTT import SMA, EMA, REF, MA, MAX, ABS, AVEDEV, CROSS, LLV, HHV
import numpy as np

class KDJ(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        J=self.JVal(df, info)
        AB= CROSS(J, 0)
        if  AB.size > 0 and AB[-1]:
            return True
        return False

    def findSell(self, df, info):
        J=self.JVal(df, info)
        AB= CROSS(100, J)
        if  AB.size > 0 and AB[-1]:
            return True
        return False

    def transactions(self, df, info):
        J=self.JVal(df, info)
        Buy=CROSS(J, 0)
        Sell=CROSS(100, J)
        return Buy, Sell

    def JVal(self, df, info):
        P1=9
        P2=3
        P3=3
        CLOSE = df.CLOSE
        LOW = df.LOW
        HIGH = df.HIGH
        with np.errstate(divide='ignore',invalid='ignore'):
            RSV=(CLOSE-LLV(LOW,P1))/(HHV(HIGH,P1)-LLV(LOW,P1))*100
            K=SMA(RSV,P2,1)
            D=SMA(K,P3,1)
            J=3*K-2*D
            return J

"""
RSV:=(CLOSE-LLV(LOW,P1))/(HHV(HIGH,P1)-LLV(LOW,P1))*100;
K:SMA(RSV,P2,1),COLORFF8D1E;
D:SMA(K,P3,1),COLOR0CAEE6;
J:3*K-2*D,COLORE970DC;

{前一天J小于0，今天J>0}
超跌確認:=REF(J,1)<0 AND J>0;
超涨確認:=REF(J,1) > 100 AND J<100;

"""