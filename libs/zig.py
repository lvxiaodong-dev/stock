import math


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
        
def GetFirstVaildIndex(data):
    count=len(data)
    for i in range(count):
        if (IsNumber(data[i])):
            return i
    
    return count

def ZIG_Calculate(data, dRate):
    nDataCount=len(data)
    dest=CreateArray(nDataCount)
    m=GetFirstVaildIndex(data)
    i, lLastPos, lState, j = 0, 0, 0, 0
    dif = 0
    lLastPos, lState = m, m
    for i in range(m+1, nDataCount-1) :
        if (lState==m):
            break
        if abs(data[i] - data[m]) * 100 >= dRate*data[m]:
            if (data[i]>data[m]) :
                lState=i
            else :
                lState=-1
        else :
            lState=m
    
    for i in range(i, nDataCount-1) :
        if (data[i] >= data[i - 1] and data[i] >= data[i + 1]) :
            if (lState<0) :
                if ((data[i] - data[-lState]) * 100<dRate*data[-lState]) :
                    continue
                else :
                    j = -lState
                    dif = (data[lLastPos] - data[j]) / (-lState - lLastPos)
                    dest[j]=data[-lState]
                    j-=1
                    for j in range(j,lLastPos-1,-1):    # for (; j >= lLastPos; j--)
                        dest[j]=data[-lState] + (-lState - j)*dif
                    lLastPos = -lState
                    lState = i
            
            elif (data[i]>data[lState]):
                lState = i
        elif (data[i] <= data[i - 1] and data[i] <= data[i + 1]) :
            if (lState>0) :
                if ((data[lState] - data[i]) * 100<dRate*data[lState]):
                    continue
                else :
                    j = lLastPos
                    dif = (data[lState] - data[j]) / (lState - lLastPos)
                    dest[j]=data[lLastPos]
                    j+=1
                    for j in range(j,lState+1) :
                        dest[j]=data[lLastPos] + (j - lLastPos)*dif
                    lLastPos = lState
                    lState = -i
            elif (data[i]<data[-lState]) :
                lState = -i

    if (abs(lState) >= nDataCount - 2) :
        if (lState>0 and data[nDataCount - 1] >= data[lState]) :
            lState = nDataCount - 1
        if (lState<0 and data[nDataCount - 1] <= data[-lState]) :
            lState = 1 - nDataCount

    if (lState>0) :
        j = lLastPos
        dif = (data[lState] - data[j]) / (lState - lLastPos )
        dest[j]=data[lLastPos]
        j+=1
        for j in range(j, lState+1) :
            dest[j]=data[lLastPos] + (j - lLastPos)*dif
    else :
        j = -lState
        dif = (data[lLastPos] - data[j]) / (-lState - lLastPos)
        dest[j]=data[-lState]
        j-=1
        for j in range(j,lLastPos-1,-1) : # for (; j >= lLastPos; j--)
            dest[j]=(data[-lState] + (-lState - j)*dif)
    
    lState = abs(lState)
    if (lState<nDataCount - 1) :
        if (data[nDataCount - 1] >= data[lState]) :
            j = lState
            dif = (data[nDataCount - 1] - data[j]) / (nDataCount - lState)
            dest[j]=(data[lState])
            j+=1
            for j in range(j, nDataCount):
                dest[j]=(data[lState] + (j - lState)*dif)
        else :
            j = nDataCount - 1
            dif = (data[lState] - data[j]) / (nDataCount - lState)
            dest[j]=(data[nDataCount - 1])
            j-=1
            for j in range(j, lState-1, -1) : #for (; j >= lState; j--)
                dest[j]=(data[nDataCount - 1] + (nDataCount - j)*dif)

    return dest


def ZIG(df, K, N) :
        if K == 0:
            K = df.OPEN
        elif K == 1:
            K = df.HIGH
        elif K == 2:
            K = df.LOW
        elif K == 3:
            K = df.CLOSE
        else:
            print('传参有误')
            return []
        
        return ZIG_Calculate(K, N)