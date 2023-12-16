import pandas as pd
from libs.MyTA import MyTA as mta
from strategy.Strategy import Strategy

class HDLY(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        df1 = self.YahooDf(df)
        dfsize=df1['Close'].size
        va=[]
        for i in range(1,min(100, dfsize)):
            c1=df1['Close'].iloc[-i]
            h1=df1['High'].iloc[-i]
            l1=df1['Low'].iloc[-i]
            o1=df1['Open'].iloc[-i]
            v1=df1['Volume'].iloc[-i]
            high_part=(h1-c1)/(h1-l1)
            body_part=(c1-o1)/(h1-l1)
            low_part=(o1-l1)/(h1-l1)
            pull_m=body_part*0.8*v1
            pull_up=high_part*0.2*v1
            pull_down=low_part*0.2*v1
            wash_m=body_part*0.2*v1
            wash_up=high_part*0.8*v1
            wash_down=low_part*0.8*v1
            z1=pull_m+pull_up+pull_down
            f1=wash_m+wash_up+wash_down
            increase=z1-f1
            try:
                if c1>df1['Close'].iloc[-i-1]:
                    va.append(v1)
                else:
                    va.append(increase)
            except Exception as ex:
                pass

        va=pd.Series(va)
        vas1=va.rolling(60,min_periods=60).max()
        a1=(va.rolling(5,min_periods=5).sum()/va.rolling(5).min())/10000
        k1=a1.rolling(3,min_periods=3).mean()
        d1=k1.rolling(3,min_periods=3).mean()
        j1=3*k1-2*d1
        retail1=(va.rolling(24,min_periods=24).max()-va.rolling(24,min_periods=24).sum())/10000/vas1

        retail=100*((df1['High'].rolling(55,min_periods=55).max()-df1['Close'].rolling(1).mean())/(df1['High'].rolling(55,min_periods=55).max()-df1['Low'].rolling(55,min_periods=55).min()))
        rsv=100*((df1['Close'].rolling(1).mean()-df1['Low'].rolling(34,min_periods=34).min())/(df1['High'].rolling(34,min_periods=34).max()-df1['Low'].rolling(34,min_periods=34).min()))
        k2=rsv.rolling(3,min_periods=3).mean()
        d2=k2.rolling(3,min_periods=3).mean()
        j2=3*k2-2*d2
        t1=retail1.dropna().reset_index(drop=True)-j1.dropna().reset_index(drop=True)
        t2=j2.reset_index(drop=True)-retail.reset_index(drop=True)
        cc1=t1.rolling(2,min_periods=2).mean()
        cc2=t2.rolling(2,min_periods=2).mean()
        # 精度小取95和-95，精度大选100
        if cc2.iloc[-1]<-99:
            return True
            #exportList_low.append(stock)
        # elif cc2.iloc[-1]>99:
        #     exportList_high.append(stock)
        return False