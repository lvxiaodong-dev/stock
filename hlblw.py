import akshare as ak
import pandas as pd
import talib as ta
import datetime as dt
import numpy as np
import math
from MyTT import *

def IsNumber(value):
    if not isinstance(value,(int,float)):
        return False
    if (math.isnan(value)):
        return False
    return True

def CreateArray(count, value=float('nan')):
        if count<=0:
            return []
        else:
            return [value]*count

def BACKSET(condition,n):
        dataCount=len(condition)
        if dataCount<=0:
            return []

        result=CreateArray(dataCount,0)   # 初始化0

        for pos in range(dataCount):
            if IsNumber(condition[pos]):
                break

        if pos==dataCount:
            return result

        num=min(dataCount-pos,max(n,1))
        for i in range(dataCount-1, -1,-1):
            value=condition[i]
            if IsNumber(value) and value:
                for j in range(i, i-num,-1):
                    result[j]=1

        if condition[i]:
            for j in range(i, pos+1):
                result[j]=1

        return result

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

start = dt.datetime(2022, 1, 1).strftime("%Y%m%d")
now = dt.datetime.now().strftime("%Y%m%d")

filepath = "A.csv"
stocklist = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = stocklist['code'].values

gold_cross_stocks=[]
for code in stock_codes:
    try:
        # 获取日线数据
        stock_data = ak.stock_zh_a_hist(symbol=code, start_date=start, end_date=now, period="daily", adjust="qfq")
        CLOSE = stock_data["收盘"]

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
        
        PERIOD_COND1 = pd.Series(PERIOD_COND1)
        COND2=pd.Series(CLOSE<REF(CLOSE,PERIOD_COND1.iat[-1]+1)) & pd.Series(TOWERC>REF(TOWERC,PERIOD_COND1.iat[-1]+1))
        COND3=COND1 & COND2;

        AA1=BACKSET(COND3,PERIOD_COND1.iat[-1]+2)
        BB1=FILTER(AA1,PERIOD_COND1.iat[-1]+1)

        
        if BB1[-1]:
            print('找到了----'+code)
            gold_cross_stocks.append(code)
        else:
            print(code)
    except Exception as e:
        print("发生了异常:", e)

file_path = "hlblw.txt"
with open(file_path, "w") as file:
    file.write('弘历背离王选股结果:\n')
    for code in gold_cross_stocks:
        line = str(code) + "\n"
        file.write(line)