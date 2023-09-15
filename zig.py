import numpy as np

def zig(df, K, N):
    ZIG_STATE_START = 0
    ZIG_STATE_RISE = 1
    ZIG_STATE_FALL = 2

    if K == 0:
        K = df['开盘']
    elif K == 1:
        K = df['最高']
    elif K == 2:
        K = df['最低']
    elif K == 3:
        K = df['收盘']
    else:
        print('传参有误')
        pass

    peer_i = 0
    candidate_i = None
    scan_i = 0
    peers = [0]
    z = np.zeros(len(K))
    state = ZIG_STATE_START
    while True:
        #print(peers)
        scan_i += 1
        if scan_i == len(K) - 1:
            # 扫描到尾部
            if candidate_i is None:
                peer_i = scan_i
                peers.append(peer_i)
            else:
                if state == ZIG_STATE_RISE:
                    if K[scan_i] >= K[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
                elif state == ZIG_STATE_FALL:
                    if K[scan_i] <= K[candidate_i]:
                        peer_i = scan_i
                        peers.append(peer_i)
                    else:
                        peer_i = candidate_i
                        peers.append(peer_i)
                        peer_i = scan_i
                        peers.append(peer_i)
            break
 
        if state == ZIG_STATE_START:
            if K[scan_i] >= K[peer_i] * (1 + N):
                candidate_i = scan_i
                state = ZIG_STATE_RISE
            elif K[scan_i] <= K[peer_i] * (1 - N):
                candidate_i = scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            if K[scan_i] >= K[candidate_i]:
                candidate_i = scan_i
            elif K[scan_i] <= K[candidate_i]*(1-N):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if K[scan_i] <= K[candidate_i]:
                candidate_i = scan_i
            elif K[scan_i] >= K[candidate_i]*(1+N):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    
    #线性插值， 计算出zig的值            
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i+1]
        start_value = K[peer_start_i]
        end_value = K[peer_end_i]
        a = (end_value - start_value)/(peer_end_i - peer_start_i)# 斜率
        for j in range(peer_end_i - peer_start_i +1):
            z[j + peer_start_i] = start_value + a*j
    return z



# AA = zig(df, 3, 0.05)
# BB = REF(zig(df, 3, 0.05), 1)

# print(AA)
# print(BB)