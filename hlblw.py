import akshare as ak
import pandas as pd
import talib as ta
import datetime as dt
import numpy as np
from MyTT import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

start = dt.datetime(2022, 1, 1).strftime("%Y%m%d")
now = dt.datetime.now().strftime("%Y%m%d")

filepath="SZ.csv"

stocklist = pd.read_csv(filepath,dtype=str,engine="python")

stock_codes = stocklist['A股代码'].values

  

for code in stock_codes:

# 获取日线数据

stock_data = ak.stock_zh_a_hist(symbol=code,start_date=start,end_date=now,period="daily",adjust="qfq")

CLOSE = stock_data["收盘"]

# 计算指标

A1=FORCAST(EMA(CLOSE,5),6)

A2=FORCAST(EMA(CLOSE,8),6)

A3=FORCAST(EMA(CLOSE,11),6)

A4=FORCAST(EMA(CLOSE,14),6)

A5=FORCAST(EMA(CLOSE,17),6)

B=A1+A2+A3+A4-4*A5

TOWERC=EMA(B,2)

  
  

FLAG=TOWERC>=REF(TOWERC,1);

FLAG1=REF(FLAG,1)

FLAG1=FLAG1[~np.isnan(FLAG1)]

print(FLAG1)

COND1=FLAG & (~FLAG1);

PERIOD_COND1=BARSLAST(REF(COND1,1));

COND2=CLOSE<REF(CLOSE,PERIOD_COND1+1) & TOWERC>REF(TOWERC,PERIOD_COND1+1);

COND3=COND1 & COND2;

  

AA1=BACKSET(COND3,PERIOD_COND1+2);

BB1=FILTER(AA1,PERIOD_COND1+1);