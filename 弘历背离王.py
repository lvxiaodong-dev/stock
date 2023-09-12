import akshare as ak 
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
from MyTT import EMA, REF, FORCAST, BARSLAST

# 是否是分钟周期类型
def is_min_period_type(period):
    return period in ['1','5','15','30','60']

period = 'daily'  #周期可选参数： 1 5 15 30 60 daily weekly monthly 

# 设置查询数据的开始时间，结束时间
start_date = '2022-08-29 00:00:00'
end_date = '2023-08-29 00:00:00'
# end_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
results = []

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
            CLOSE = df['收盘']
            A1 = FORCAST(EMA(CLOSE, 5), 6)
            A2 = FORCAST(EMA(CLOSE, 8), 6)
            A3 = FORCAST(EMA(CLOSE, 11), 6)
            A4 = FORCAST(EMA(CLOSE, 14), 6)
            A5 = FORCAST(EMA(CLOSE, 17), 6)
            B = A1+A2+A3+A4-4*A5
            TOWERC = EMA(B, 2)
            
            FLAG = TOWERC >= REF(TOWERC, 1)
            FLAG1 = pd.Series(REF(FLAG, 1)).bfill()
            COND1 = FLAG & (~FLAG1)
            PERIOD_COND1 = BARSLAST(REF(COND1,1));
            COND2 = (CLOSE.iat[-1] < REF(CLOSE, PERIOD_COND1[-1] + 1)[-1]) & (TOWERC[-1] > REF(TOWERC, PERIOD_COND1[-1] + 1)[-1])
            
            # 记录结果
            if COND1.iat[-1] & COND2:
                results.append(df_a.loc[index].tolist())
                
        except Exception as e:
            pass
            
# 一次性写入文件
np.savetxt(f'弘历背离王_{period}_{end_date}.txt', results, delimiter=',', fmt='%s')