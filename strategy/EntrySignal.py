import pandas as pd
import talib as ta
from strategy.Strategy import Strategy
from MyTT import MAX,ABS,REF,EMA,SMA,MA,LLV,HHV,CROSS

# 建仓信号
class EntrySignal(Strategy):
  def __init__(self, *args):
    super().__init__(*args)

  def find(self):
    df = self.df
    CLOSE = df.CLOSE
    OPEN = df.OPEN
    LOW = df.LOW
    HIGH = df.HIGH

    MTR=MAX(MAX((HIGH-LOW),ABS(REF(CLOSE,1)-HIGH)),ABS(REF(CLOSE,1)-LOW));
    ATR=EMA(MTR,30); 
    UPOS=HIGH+ATR*0.5;
    DPOS=LOW-ATR*0.5;
    N=3; 
    A1=CLOSE>REF(CLOSE,4);
    B1=CLOSE<REF(CLOSE,4);


    A=(3*CLOSE+LOW+OPEN+HIGH)/6;
    X=(20*A+19*REF(A,1)+18*REF(A,2)+17*REF(A,3)+16*REF(A,4)+15*REF(A,5)+14*REF(A,6)+13*REF(A,7)+12*REF(A,8)+11*REF(A,9)+10*REF(A,10)+9*REF(A,11)+8*REF(A,12)+7*REF(A,13)+6*REF(A,14)+5*REF(A,15)+4*REF(A,16)+3*REF(A,17)+2*REF(A,18)+REF(A,20))/210;
    S2=SMA(CLOSE,3,1);
    S6=SMA(CLOSE,5,1);
    DK=2*(S2-S6);

    MA5=MA(CLOSE,5);
    MA10=MA(CLOSE,10);
    MA30=MA(CLOSE,30);
    VAR1=LLV(LOW,21);
    VAR2=HHV(HIGH,21);
    AK1=EMA((((CLOSE - VAR1) / (VAR2 - VAR1)) * 100),5);
    AK=EMA((((CLOSE - VAR1) / (VAR2 - VAR1)) * 50),13);
    AB=CROSS(AK1,AK);
    
    # 判断金叉
    if AB[-1]:
      return True
    return False
  