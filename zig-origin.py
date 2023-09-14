
# coding: utf-8 
"""
Created on Sat Jan 05 18:53:39 2019
http://www.pianshen.com/article/363258879/
@author: duanqs
"""

import numpy as np
import akshare as ak

import matplotlib.pyplot as plt
 
ZIG_STATE_START = 0
ZIG_STATE_RISE = 1
ZIG_STATE_FALL = 2
 
 
def zig(x=0.055):
    #ts.set_token("此处放入tushare的token！！！")
    #pro = ts.pro_api()
    #df = pro.daily(ts_code="603297.SH")
    # print(list(df["close"]))
    # df = ts.get_hist_data('000069')
    # df = df[::-1]
    # 获取股票交易数据的Tushare的使用方法 - 蜗牛爬行ing - 博客园  
    # https://www.cnblogs.com/DreamRJF/p/8660630.html
    # posted on 2018-03-28 15:18 蜗牛爬行ing 
    
    #df = ts.get_k_data('000069')
    # df = ts.get_k_data('600535')
    # df = ts.get_k_data('512040')  # 富国国信价值 etf 基金
    # df = ts.get_h_data('000051', index=True)   # 上证180等权指数 index 参数必须指定为True
    df = ak.stock_zh_a_hist(symbol='600257', start_date=20220101, end_date=20230913, period='daily', adjust="qfq")

    
    #df = ts.get_h_data('399106', index=True)   # index 参数必须指定为True
    #df = ts.get_h_data('399106', index=True) #深圳综合指数
    #df = ts.get_k_data('399106', index=True) #深圳综合指数
    # df = ts.get_k_data('931052', index=True) # 中证国信价值指数， 不支持的指数
    # df = ts.get_k_data('hs300')   # 支持主要的几个股票指数的历史行情
    # 股票代码，即6位数字代码，或者指数代码
    # （sh=上证指数 sz=深圳成指 hs300=沪深300指数 
    # sz50=上证50 zxb=中小板 cyb=创业板）
    
    
    
    #df = df.reset_index(drop=True)
    # df = df.iloc[-100:]
    #x = 0.055
    k = df["收盘"]
    #d = df["trade_date"]
    d = df['日期']
    # d = df.index
    #print(k)
    #print(d)
    # 循环前的变量初始化
    # 端点 候选点 扫描点 端点列表 拐点线列表 趋势状态
    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
        #print(peers)
        scan_i += 1
        if scan_i == len(k) - 1:
            # 扫描到尾部
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= k[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
 
        if state == ZIG_STATE_START:
            if k[scan_i] >= k[peer_i] * (1 + x):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - x):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i]*(1-x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i]*(1+x):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    
    #线性插值， 计算出zig的值            
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i+1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value)/(peer_end_i - peer_start_i)# 斜率
        for j in range(peer_end_i - peer_start_i +1):
            z[j + peer_start_i] = start_value + a*j
    
    print(u'...转向点的阀值、个数、位置和日期...')        
    print(x, len(peers))
    print(peers)
    dates = [d[i] for i in peers]
    print(dates)
    #print([k[i] for i in peers])
    #print(list(k))
    #print(list(z))
    
    plt.plot(z)
 
zig(x=0.055)

