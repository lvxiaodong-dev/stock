import akshare as ak 
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
import talib
from MyTT import EMA, REF, FORCAST, BARSLAST,LLV,HHV,SMA,MA,AVEDEV

def TROUGHBARS(df, K, N, M):
    df['min'] = df[K].rolling(window=N).min()
    df['is_trough'] = df[K].shift(-1) > df['min']
    trough_points = df[df['is_trough']].index.tolist()
    future_trough_points = [i-M for i in trough_points]
    df['TROUGHBARS'] = df.index.to_series().apply(lambda x: min([abs(x-i) for i in future_trough_points], default=0))
    return df['TROUGHBARS']

def ZIG(df, K, N):
    df['pct_change'] = df[K].pct_change() * 100
    df['ZIG'] = df['pct_change'][df['pct_change'].abs() > N]
    return df['ZIG']

# 是否是分钟周期类型
def is_min_period_type(period):
    return period in ['1','5','15','30','60']

period = 'daily'  #周期可选参数： 1 5 15 30 60 daily weekly monthly 

# 设置查询数据的开始时间，结束时间
start_date = '2021-01-01 00:00:00'
end_date = '2023-5-29 15:00:00'
# end_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

##兼容开始时间、结束时间
if ~is_min_period_type(period):
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    start_date = start_date.strftime("%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    end_date = end_date.strftime("%Y%m%d")

# 获取股票代码
filepath = "CS.csv"
df_a = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_a['code'].values

# 创建数组存储结果
results = [df_a.columns.tolist()]

with tqdm(total=len(stock_codes)) as progress_bar:
    # 遍历查找股票
    for index,code in enumerate(stock_codes):
        progress_bar.update(1)
        # try:
        # 获取数据
        if is_min_period_type(period):
            df = ak.stock_zh_a_hist_min_em(symbol=code, start_date=start_date, end_date=end_date, period=period, adjust="qfq")
        else:
            df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period=period, adjust="qfq")
        
        # 向量化计算指标
        CLOSE = df['收盘']
        HIGH = df['最高']
        LOW = df['最低']
        N=9;
        M1=3;
        M2=3;
        RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K=SMA(RSV,M1,1)
        D=SMA(K,M2,1)
        VAR1=(HIGH+LOW+CLOSE)/3;
        VAR2=(VAR1-MA(VAR1,14))/(0.015*AVEDEV(VAR1,14));
        print(int(HIGH.iat[-1]) > (int(LOW.iat[-1]) + 0.04))
        VAR3 = 80 
        if ((int(TROUGHBARS(df, '最低', 3, 16).iat[-1]) == 0) and (HIGH.iat[-1] > (LOW.iat[-1]) + 0.04)) else 0
        VAR4=50 if((ZIG(df, '收盘', 3)>REF(ZIG(df, '收盘', 3),1)).iat[-1] & (REF(ZIG(df, '收盘', 3),1)<=REF(ZIG(df, '收盘', 3),2))[-1] & (REF(ZIG(df, '收盘', 3),2)<=REF(ZIG(df, '收盘', 3),3))[-1]) else 0;
        if VAR2.iat[-1]<-110 & VAR3>0:
            print('★掘底买点')

        if VAR2.iat[-1]<-110 & VAR4>0:
            print('★黑马信号')
            
        # except Exception as e:
        #     print(e)
            
# 一次性写入文件
# np.savetxt(f'hlblw_{period}_{end_date}.txt', results, delimiter=',', fmt='%s')