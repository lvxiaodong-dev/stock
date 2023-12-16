import talib as ta
from strategy.Strategy import Strategy
from MyTT import ABS,REF,LAST,BARSLAST,MA,EVERY,HHV,LLV 

class EYZZ(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        try:
            CLOSE = df.CLOSE
            L = df.LOW
            H = df.HIGH
            N=14

            UPPER, MID, LOWER = ta.BBANDS(CLOSE, timeperiod =20)
            MA60=MA(CLOSE, 60)
            F0=REF(UPPER,1)-REF(MID,1)
            F1=ABS(F0)

            F0=REF(MID,1)-REF(LOWER,1)
            F2=ABS(F0)
            
            F0=F1/F2
            F1=F0<1.1
            C0=EVERY(F1,14)

            F0=UPPER>REF(UPPER,1)
            F1=EVERY(F0,2)
            F0=MID>REF(MID,1)
            F2=EVERY(F0,2)
            F0=LOWER<REF(LOWER,1)
            F3=EVERY(F0,2)
            F0=F1&F2
            C1=F0&F3

            F0=HHV(H,N)
            F11=REF(F0,1)
            F2=LLV(L,N)
            F3=REF(F2,1)
            F4=F11-F3
            F0=LLV(L,N)
            F1=REF(F0,1)
            F2=F4/F1
            振幅=F2*100 
            C2=振幅<25

            C3=CLOSE>F11
            
            F0=CLOSE>UPPER
            CX1=REF(CLOSE,1)
            F1=CX1<UPPER
            C4=F0&F1

            MIDX1=REF(MID,1)
            F0=MID>MIDX1
            MA60X1=REF(MA60,1)
            F1=MA60>MA60X1
            C5=F0 & F1

            F0=C0&C1
            F1=F0&C2
            F2=F1&C3
            F3=F2&C4
            EEZZ=F3&C5
            if EEZZ.iloc[-1]:
                return True
            return False
        except IndexError:
            return False

''''
{此指标根据2023年12月05日 JOSIE 的铁粉课程所讲的“鳄鱼张嘴”战法而写成。}
{布林带}
DIS:=STDP(CLOSE,20);
MID:MA(CLOSE,20),COLORFFAEC9;
UPPER:MID+2*DIS,COLORFFC90E;
LOWER:MID-2*DIS,COLOR0CAEE6;

{20日和60日均线}
MA20:=MA(C,20);
MA60:=MA(C,60);

{鳄鱼张嘴}
C0:=EVERY(ABS(REF(UPPER,1)-REF(MID,1))/ABS(REF(MID,1)-REF(LOWER,1))<1.1,N); {过去N日上下轨与中轨的距离均不高于10%}
C1:=EVERY(UPPER>REF(UPPER,1),2) AND EVERY(MID>REF(MID,1),2) AND EVERY(LOWER<REF(LOWER,1),2); {过去两天，每日的上轨和中轨均高于前一天，下轨均低于前一天}
振幅:=(REF(HHV(H,N),1)-REF(LLV(L,N),1))/REF(LLV(L,N),1)*100; {过去N日振幅算法}
C2:=振幅<25; {过去N日股价振幅不高于25%}
C3:=C>REF(HHV(H,N),1); {收盘价高于过去N日内最高价}
C4:=C>UPPER AND REF(C,1)<UPPER;
C5:=MA20>REF(MA20,1) AND MA60>REF(MA60,1); {MA20和MA60均上升}
鳄鱼张嘴:=C0 AND C1 AND C2 AND C3 AND C4 AND C5;

STICKLINE(鳄鱼张嘴 AND EVERY(NOT(REF(鳄鱼张嘴,1)),5),O,C,0.65,0),COLORWHITE;
DRAWICON(鳄鱼张嘴 AND EVERY(NOT(REF(鳄鱼张嘴,1)),5),H*1.02,5);
DRAWTEXT(鳄鱼张嘴 AND EVERY(NOT(REF(鳄鱼张嘴,1)),5),L,'                  -------------'),COLORLIGRAY; {以鳄鱼张嘴买入K线的最低价为止损线}
'''