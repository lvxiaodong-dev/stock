
import numpy as np
import math
import copy

def IsNumber(value):
        if not isinstance(value,(int,float)) :
            return False
        if (math.isnan(value)):
            return False
        return True

def CreateArray(count, value=float('nan')) :
        if count<=0 :
            return []
        else :
            return [value]*count

# 获取第1个有效数据索引
def GetFirstVaildIndex(data):
    count=len(data)
    for i in range(count):
        if (IsNumber(data[i])):
            return i
    
    return count

def ZIG(df, K, N):
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
            if K[scan_i] > K[candidate_i]:
                candidate_i = scan_i
            elif K[scan_i] <= K[candidate_i]*(1-N):
                peer_i = candidate_i
                peers.append(peer_i)
                state = ZIG_STATE_FALL
                candidate_i = scan_i
        elif state == ZIG_STATE_FALL:
            if K[scan_i] < K[candidate_i]:
                candidate_i = scan_i
            elif K[scan_i] >= K[candidate_i]*(1+N):
                peer_i = candidate_i
                # peers.append(peer_i)
                state = ZIG_STATE_RISE
                candidate_i = scan_i
    result = [False] * len(K)
    for i in peers:
        result[i] = True
    return result


def TROUGHBARS(df, K, N, M):
    zigData=ZIG(df, K, N)   # 计算ZIG
    lEnd=M
    if (lEnd<1) :
        return []

    nDataCount = len(zigData)
    dest=CreateArray(nDataCount)
    trough = CreateArray(lEnd, 0)
    lFlag = 0
    i = GetFirstVaildIndex(zigData) + 1
    lEnd-=1
    while i<nDataCount and zigData[i]>zigData[i - 1] :
        i+=1
    
    while i<nDataCount and zigData[i]<zigData[i - 1] :
        i+=1

    i-=1
    trough[0] = i
    for i in range(i, nDataCount - 1) :
        if (zigData[i]<zigData[i + 1]) :
            if (lFlag) :
                if (lEnd) :
                    tempTrough=copy.deepcopy(trough)
                    for j in range(lEnd) :
                        trough[j+1]=tempTrough[j]
                lFlag = 0
                trough[lFlag] = i
        else :
            lFlag = 1
        if (trough[lEnd]) :
            dest[i]=(i - trough[lEnd])

    if (trough[lEnd]) :
        dest[i]=(i - trough[lEnd])

    return dest