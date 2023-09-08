import akshare as ak
import talib as ta 

# 获取A股数据
stock_df = ak.stock_zh_a_daily(symbol='sh000001') 

# 计算指标
ema5 = ta.EMA(stock_df['close'], timeperiod=5)
ema8 = ta.EMA(stock_df['close'], timeperiod=8)  
ema11 = ta.EMA(stock_df['close'], timeperiod=11)
ema14 = ta.EMA(stock_df['close'], timeperiod=14)
ema17 = ta.EMA(stock_df['close'], timeperiod=17)

a1 = ta.LINEARREG(ema5, 6)  
a2 = ta.LINEARREG(ema8, 6)
a3 = ta.LINEARREG(ema11, 6)
a4 = ta.LINEARREG(ema14, 6)
a5 = ta.LINEARREG(ema17, 6)

b = a1 + a2 + a3 + a4 - 4*a5
towerc = ta.EMA(b, 2)

# 找背离
flag = towerc >= towerc.shift(1)
cond1 = flag & (~flag.shift(1))
cond2 = stock_df['close'] < stock_df['close'].shift(cond1.cumsum()) 
cond2 = cond2 & (towerc > towerc.shift(cond1.cumsum()))
cond3 = cond1 & cond2

# 绘制图形
# 略...

# 获取所有A股数据筛选背离股票
all_stocks = ak.stock_zh_a_spot()
diverg_stocks = []

for symbol in all_stocks['code']:
    stock_df = ak.stock_zh_a_daily(symbol=symbol)  
    # 计算指标,筛选背离股票
    if cond3.any():
        diverg_stocks.append(symbol)

print(diverg_stocks)