import akshare as ak
import pandas as pd
import talib as ta
import datetime as dt
import numpy as np
from tqdm import tqdm
from MyTT import *

start_date = dt.datetime(2022, 1, 1).strftime("%Y%m%d")
end_date = dt.datetime(2023, 8, 25).strftime("%Y%m%d")
# end_date = dt.datetime.now().strftime("%Y%m%d")

filepath = "A.csv"
stocklist = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = stocklist['code'].values

progress_bar = tqdm(total=len(stock_codes))

gold_cross_stocks=[]
for code in stock_codes:
    progress_bar.update(1)
    try:
        # 获取日线数据
        stock_data = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period="daily", adjust="qfq")
        CLOSE = stock_data['收盘']

        # 计算指标
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
        
        if COND1.iat[-1] & COND2:
            print('找到了背离----'+code+'----')
            gold_cross_stocks.append(code)
    except Exception as e:
        # 获取异常信息
        exception_type = type(e).__name__  # 异常类型的名称
        exception_message = str(e)  # 异常的具体描述信息

        # 打印异常信息
        print("异常类型:", exception_type)
        print("异常信息:", exception_message)

file_path = "hlblw.txt"
with open(file_path, "w") as file:
    file.write('弘历背离王选股结果:\n')
    for code in gold_cross_stocks:
        line = str(code) + "\n"
        file.write(line)

progress_bar.close()