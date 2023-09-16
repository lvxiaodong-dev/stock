import akshare as ak 
from datetime import datetime
from tqdm import tqdm
import numpy as np
import pandas as pd
from MyTT import REF,LLV,HHV,LLV,SMA,AVEDEV,MA
from zig import ZIG
from troughbars import TROUGHBARS

# 是否是分钟周期类型
def is_min_period_type(period):
    return period in ['1','5','15','30','60']

period = 'daily'  #周期可选参数： 1 5 15 30 60 daily weekly monthly 

# 设置查询数据的开始时间，结束时间
start_date = '2019-01-01 00:00:00'
end_date = '2023-09-04 15:00:00'
# end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

##兼容开始时间、结束时间
if ~is_min_period_type(period):
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    start_date = start_date.strftime("%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    end_date = end_date.strftime("%Y%m%d")

# 获取股票代码
filepath = "A.csv"
df_a = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_a['code'].values

# 创建数组存储结果
results1 = []
results2 = []
results3 = []

with tqdm(total=len(stock_codes)) as progress_bar:
    # 遍历查找股票
    for index,code in enumerate(stock_codes):
        progress_bar.update(1)
        try:
            # 获取数据
            if is_min_period_type(period):
                df = ak.stock_zh_a_hist_min_em(symbol=code, start_date=start_date, end_date=end_date, period=period, adjust="qfq")
            else:
                df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period=period, adjust="qfq")
            
            # 向量化计算指标
            OPEN = df['开盘']
            CLOSE = df['收盘']
            HIGH = df['最高']
            LOW = df['最低']

            N=9;
            M1=3;
            M2=3;
            VAR1=(HIGH+LOW+CLOSE)/3;
            VAR2=(VAR1-MA(VAR1,14))/(0.015*AVEDEV(VAR1,14));
            VAR3 = False
            z = ZIG(df, 3, 22)
            VAR3 = 1 if TROUGHBARS(df, 3, 0.16, 1)[-2] == 1 and (HIGH.iat[-1]>LOW.iat[-1]+0.04) else 0
            VAR4= 1 if (z[-1]>z[-2] and z[-2]<=z[-3] and z[-3]<=z[-4]) else 0
            
            if VAR2.iat[-2]<-110 and VAR3 == 1:
                print('★掘底买点:' + code)
                results1.append(df_a.loc[index].tolist())

            if VAR2.iat[-2]<-110 and VAR4 == 1:
                print('★黑马信号:' + code)
                results2.append(df_a.loc[index].tolist())
            if VAR2.iat[-2]<-110 and VAR3 == 1and VAR4 == 1:
                results3.append(df_a.loc[index].tolist())
        except Exception as e:
            print(e)
            
# 一次性写入文件
np.savetxt(f'黑马_掘底买点_{period}_{end_date}.txt', results1, delimiter=',', fmt='%s')
np.savetxt(f'黑马_黑马信号_{period}_{end_date}.txt', results2, delimiter=',', fmt='%s')
np.savetxt(f'黑马_黑马信号+掘底买点_{period}_{end_date}.txt', results3, delimiter=',', fmt='%s')