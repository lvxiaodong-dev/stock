import akshare as ak 
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
import talib
import copy
from my_help import JSComplierHelper
from MyTT import EMA, REF, FORCAST, BARSLAST,LLV,HHV,SMA,MA,AVEDEV

# 属于未来函数,之字转向.
# 用法: ZIG(K,N),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,其余:数组信息
# 例如: ZIG(3,5)表示收盘价的5%的ZIG转向
def ZIG(K,N) :
    if JSComplierHelper.IsNumber(K):
        if K==0 :
            K=OPEN
        elif K==1 :
            K= HIGH
        elif K==2 :
            K=LOW
        elif K==3:
            K=CLOSE
        else :
            return []
    
    return ZIG_Calculate(K,N)

# 获取第1个有效数据索引
def GetFirstVaildIndex(data):
    count=len(data)
    for i in range(count):
        if (JSComplierHelper.IsNumber(data[i])):
            return i
    
    return count

def ZIG_Calculate(data,dRate):
    nDataCount=len(data)
    dest=JSComplierHelper.CreateArray(nDataCount)
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

def TROUGHBARS(data,n,n2) :
        zigData=ZIG(data,n)   # 计算ZIG
        lEnd=n2
        if (lEnd<1) :
            return []

        nDataCount = len(zigData)
        dest=JSComplierHelper.CreateArray(nDataCount)
        trough = JSComplierHelper.CreateArray(lEnd,0)
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


# 是否是分钟周期类型
def is_min_period_type(period):
    return period in ['1','5','15','30','60']

period = 'daily'  #周期可选参数： 1 5 15 30 60 daily weekly monthly 

# 设置查询数据的开始时间，结束时间
start_date = '2021-01-01 00:00:00'
end_date = '2023-5-29 15:00:00'
# end_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

##兼容开始时间、结束时间
if ~is_min_period_type(period):
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    start_date = start_date.strftime("%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    end_date = end_date.strftime("%Y%m%d")

# 获取股票代码
filepath = "CS.csv"
df_a = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_a['code'].values

# 创建数组存储结果
results = [df_a.columns.tolist()]

with tqdm(total=len(stock_codes)) as progress_bar:
    # 遍历查找股票
    for index,code in enumerate(stock_codes):
        progress_bar.update(1)
        # try:
        # 获取数据
        if is_min_period_type(period):
            df = ak.stock_zh_a_hist_min_em(symbol=code, start_date=start_date, end_date=end_date, period=period, adjust="qfq")
        else:
            df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period=period, adjust="qfq")
        
        # 向量化计算指标
        OPEN = df['开盘']
        CLOSE = df['收盘']
        HIGH = df['最高']
        LOW = df['最低']

        N=9;
        M1=3;
        M2=3;
        RSV=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K=SMA(RSV,M1,1)
        D=SMA(K,M2,1)
        VAR1=(HIGH+LOW+CLOSE)/3;
        VAR2=(VAR1-MA(VAR1,14))/(0.015*AVEDEV(VAR1,14));
        VAR3 = 0
        if ((TROUGHBARS(LOW, 3, 16)[-1] == 0) and (HIGH>LOW+0.04).iat[-1]):
            VAR3 = 80
        VAR4=0 
        if((ZIG(CLOSE, 3)>REF(ZIG(CLOSE, 3),1))[-1] & (REF(ZIG(CLOSE, 3),1)<=REF(ZIG(CLOSE, 3),2))[-1] & (REF(ZIG(CLOSE, 3),2)<=REF(ZIG(CLOSE, 3),3))[-1]):
             VAR3 = 50
        if VAR2.iat[-1]<-110 & VAR3>0:
            print('★掘底买点')

        if VAR2.iat[-1]<-110 & VAR4>0:
            print('★黑马信号')
            
        # except Exception as e:
        #     print(e)
            
# 一次性写入文件
# np.savetxt(f'hlblw_{period}_{end_date}.txt', results, delimiter=',', fmt='%s')