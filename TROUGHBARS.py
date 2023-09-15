
import akshare as ak
from MyTT import EMA, REF, FORCAST, BARSLAST
import numpy as np
from zig import zig


df = ak.stock_zh_a_hist(symbol='600257', start_date=20220101, end_date=20230913, period='daily', adjust="qfq")


def troughbars(df, K, N, M):
    """
    TROUGHBARS函数实现
    输入:
        df - 数据DataFrame
        K - 使用的数据类型,0代表开盘价,2代表最低价
        N - ZIG转向的幅度
        M - 前M个谷点
    返回:
        periods - 前M个谷点到当前周期数的列表
    """  
    periods = []
    
    z = zig(df, K, N) # 调用zig函数获取ZIG值
    
    trough_points = [] # 谷点列表
    for i in range(1, len(z)):
        if z[i] < z[i-1] and z[i] < z[i+1]: # 找到谷点
            trough_points.append(i)
            
    for j in range(min(len(trough_points), M)):
        period = len(z) - trough_points[-j] # 计算周期数
        periods.append(period)
        
    return periods

print(troughbars(df, 3, 0.05, 1))