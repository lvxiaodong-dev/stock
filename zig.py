import numpy as np
import akshare as ak
from MyTT import EMA, REF, FORCAST, BARSLAST
 
df = ak.stock_zh_a_hist(symbol='600257', start_date=20220101, end_date=20230913, period='daily', adjust="qfq")

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
                # peers.append(peer_i)
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
    
    # print([df['日期'][i] for i in peers])

    # print([df['收盘'][i] for i in peers])


    result = [False] * len(k)
    for i in peers:
        result[i] = True
    return result
    
AA = ZIG(df, 0.05)
BB = REF(ZIG(df, 0.05), 1)
print(AA)
print(BB)
result = []
prev = -1
for i, v in enumerate(AA):
    if v:
        prev = i 
        result.append(0)
    else:
        result.append(i - prev)

# print(result)
# print(REF(ZIG(df, 0.05),1))