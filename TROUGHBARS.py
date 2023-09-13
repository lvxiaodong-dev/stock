import numpy as np
import akshare as ak
 
df = ak.stock_zh_a_hist(symbol='600257', start_date=20220101, end_date=20230901, period='daily', adjust="qfq")


def ZIG(df, N):
    ZIG_STATE_START = 0
    ZIG_STATE_RISE = 1
    ZIG_STATE_FALL = 2

    k = df["收盘"]
    d = df['日期']

    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    while True:
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
            if k[scan_i] >= k[peer_i] * (1 + N):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif k[scan_i] <= k[peer_i] * (1 - N):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if k[scan_i] >= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] <= k[candidate_i]*(1-N):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if k[scan_i] <= k[candidate_i]:
                candidate_i = scan_i
            elif k[scan_i] >= k[candidate_i]*(1+N):
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
    
    

    return [df['收盘'][i] for i in peers]
    

def TROUGHBARS(df, N, M):
    ZIG_vals = ZIG(df, N) # 调用ZIG函数获取转折点
    troughbars = np.zeros(len(df))
    trough_count = 0
    
    for i in range(len(ZIG_vals)-1):
        if ZIG_vals[i] > ZIG_vals[i+1]: # 找到谷底
            trough_count += 1
            if trough_count <= M:
                start_i = df[df['收盘'] == ZIG_vals[i]].index[0] 
                for j in range(start_i, len(df)):  
                    troughbars[j] = trough_count 

    return troughbars

print(ZIG(df, 0.05))
print(TROUGHBARS(df, 0.05, 1))