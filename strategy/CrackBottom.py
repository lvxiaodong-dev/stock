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
  

  import mytt
___________________
mytt.STICKLINE((1==1),0,9,1,0),mytt.COLORWHITE
N1 = 3
N2 = 5 
N3 = 8
N4 = 13

# 1. MACD 
DIFF = mytt.EMA(mytt.CLOSE,N3) - mytt.EMA(mytt.CLOSE,N4) 
DEA = mytt.EMA(DIFF,N2)
mytt.DRAWTEXT((DIFF>DEA),1,'●'),mytt.COLORBLUE,mytt.LINETHICK1  
mytt.DRAWTEXT((DIFF<DEA),1,'●'),mytt.COLORRED,mytt.LINETHICK1
A1 = DIFF>DEA

# 2. KDJ
RSV1 = (mytt.CLOSE-mytt.LLV(mytt.LOW,N3))/(mytt.HHV(mytt.HIGH,N3)-mytt.LLV(mytt.LOW,N3))*100
K = mytt.SMA(RSV1,N1,1) 
D = mytt.SMA(K,N1,1)
mytt.DRAWTEXT((K>D),2,'●'),mytt.COLORBLUE,mytt.LINETHICK3
mytt.DRAWTEXT((K<D),2,'●'),mytt.COLORRED,mytt.LINETHICK1
A2 = K>D

# 3. RSI
LC = mytt.REF(mytt.CLOSE,1)
RSI1 = (mytt.SMA(mytt.MAX(mytt.CLOSE-LC,0),N2,1))/(mytt.SMA(mytt.ABS(mytt.CLOSE-LC),N2,1))*100
RSI2 = (mytt.SMA(mytt.MAX(mytt.CLOSE-LC,0),N4,1))/(mytt.SMA(mytt.ABS(mytt.CLOSE-LC),N4,1))*100
mytt.DRAWTEXT((RSI1>RSI2),3,'●'),mytt.COLORBLUE,mytt.LINETHICK3  
mytt.DRAWTEXT((RSI1<RSI2),3,'●'),mytt.COLORRED,mytt.LINETHICK1
A3 = RSI1>RSI2

# 4. LWR 
RSV = -(mytt.HHV(mytt.HIGH,N4)-mytt.CLOSE)/(mytt.HHV(mytt.HIGH,N4)-mytt.LLV(mytt.LOW,N4))*100
LWR1 = mytt.SMA(RSV,N1,1)
LWR2 = mytt.SMA(LWR1,N1,1)
mytt.DRAWTEXT((LWR1>LWR2),4,'●'),mytt.COLORBLUE,mytt.LINETHICK3
mytt.DRAWTEXT((LWR1<LWR2),4,'●'),mytt.COLORRED,mytt.LINETHICK1  
A4 = LWR1>LWR2

# 5. BBI
BBI = (mytt.MA(mytt.CLOSE,N1)+mytt.MA(mytt.CLOSE,N2)+mytt.MA(mytt.CLOSE,N3)+mytt.MA(mytt.CLOSE,N4))/4
mytt.DRAWTEXT((mytt.CLOSE>BBI),5,'●'),mytt.COLORBLUE,mytt.LINETHICK3  
mytt.DRAWTEXT((mytt.CLOSE<BBI),5,'●'),mytt.COLORRED,mytt.LINETHICK1
A5 = mytt.CLOSE>BBI

# 6. MTM
MTM = mytt.CLOSE - mytt.REF(mytt.CLOSE,1)
MMS = 100*mytt.EMA(mytt.EMA(MTM,N2),N1)/mytt.EMA(mytt.EMA(mytt.ABS(MTM),N2),N1)  
MMM = 100*mytt.EMA(mytt.EMA(MTM,N4),N3)/mytt.EMA(mytt.EMA(mytt.ABS(MTM),N4),N3)
mytt.DRAWTEXT((MMS>MMM),6,'●'),mytt.COLORBLUE,mytt.LINETHICK3
mytt.DRAWTEXT((MMS<MMM),6,'●'),mytt.COLORRED,mytt.LINETHICK1
A6 = MMS>MMM

# 7. MMS
WJ = (mytt.H+mytt.L+mytt.C)/3
V1 = mytt.IF(mytt.H==mytt.L,1,mytt.H-mytt.MAX(mytt.O,mytt.C))  
V2 = mytt.IF(mytt.H==mytt.L,1,mytt.MAX(mytt.C,mytt.O)-WJ)
V3 = mytt.IF(mytt.H==mytt.L,1,mytt.MIN(mytt.O,mytt.C)-mytt.L)
V4 = mytt.IF(mytt.H==mytt.L,1,WJ-mytt.MIN(mytt.C,mytt.O))
V5 = mytt.VOL/mytt.IF(mytt.H==mytt.L,4,mytt.H-mytt.L)
V6 = (V1*V5)
V7 = (V2*V5) 
V8 = (V3*V5)
V9 = (V4*V5)
BUY_PRESSURE = (V9+V8) 
SELL_PRESSURE = (V6+V7)
DIFF_PRESSURE = BUY_PRESSURE-SELL_PRESSURE
DDX = DIFF_PRESSURE
DX = mytt.MA(DIFF_PRESSURE,5)*20
DDX1 = mytt.SMA(DX,3,1)
DDX2 = mytt.SMA(DDX1,3,1)
DDX3 = (5*DDX2+4*mytt.REF(DDX2,1)+3*mytt.REF(DDX2,2)+2*mytt.REF(DDX2,3)+mytt.REF(DDX2,4))/15
mytt.DRAWTEXT((DDX1>DDX2),7,'●'),mytt.COLORBLUE,mytt.LINETHICK3
mytt.DRAWTEXT((DDX1<DDX2),7,'●'),mytt.COLORRED,mytt.LINETHICK1
A7 = DDX1>DDX2

# 8. KDJ2
RSV2 = (mytt.CLOSE-mytt.LLV(mytt.LOW,40))/(mytt.HHV(mytt.HIGH,40)-mytt.LLV(mytt.LOW,40))*100  
K1 = mytt.SMA(RSV2,18,1)
D1 = mytt.SMA(K1,3,1) 
J1 = 3*K1-2*D1
K11 = J1>mytt.REF(J1,1) 
D11 = J1<mytt.REF(J1,1)
mytt.DRAWTEXT((K11>D11),8,'●'),mytt.COLORBLUE,mytt.LINETHICK3
mytt.DRAWTEXT((K11<D11),8,'●'),mytt.COLORRED,mytt.LINETHICK1
A8 = K11>D11

# 9. TURNOVER RATE
TURNOVERRATE = mytt.V/mytt.CAPITAL*100
VAR1 = mytt.VOL/((mytt.HIGH-mytt.LOW)*2-mytt.ABS(mytt.CLOSE-mytt.OPEN))
BUY_PRESSURE1 = mytt.IF(mytt.CLOSE>mytt.OPEN,VAR1*(mytt.HIGH-mytt.LOW),mytt.IF(mytt.CLOSE<mytt.OPEN,VAR1*((mytt.HIGH-mytt.OPEN)+(mytt.CLOSE-mytt.LOW)),mytt.VOL/2)) 
SELL_PRESSURE1 = mytt.IF(mytt.CLOSE>mytt.OPEN,0-VAR1*((mytt.HIGH-mytt.CLOSE)+(mytt.OPEN-mytt.LOW)),mytt.IF(mytt.CLOSE<mytt.OPEN,0-VAR1*(mytt.HIGH-mytt.LOW),0-mytt.VOL/2))
DLX = (BUY_PRESSURE1-(-SELL_PRESSURE1))/mytt.VOL*TURNOVERRATE
DLX1 = mytt.SUM(DLX,6)  
DLX2 = mytt