import akshare as ak
import talib

# 使用akshare获取A股股票数据
stock_zh_a_spot_df = ak.stock_zh_a_spot_em()
df = stock_zh_a_spot_df[['代码', '最新价']].rename(columns={'代码': 'code', '最新价': 'close'})

# 获取历史收盘价
close = df['close'].astype(float).values

# 计算指标
ema5 = talib.EMA(close, timeperiod=5)  # EMA(CLOSE, 5)
ema8 = talib.EMA(close, timeperiod=8)  # EMA(CLOSE, 8)
ema11 = talib.EMA(close, timeperiod=11)  # EMA(CLOSE, 11)
ema14 = talib.EMA(close, timeperiod=14)  # EMA(CLOSE, 14)
ema17 = talib.EMA(close, timeperiod=17)  # EMA(CLOSE, 17)

a1 = talib.LINEARREG(ema5, timeperiod=6)  # FORCAST(EMA(CLOSE, 5), 6)
a2 = talib.LINEARREG(ema8, timeperiod=6)  # FORCAST(EMA(CLOSE, 8), 6)
a3 = talib.LINEARREG(ema11, timeperiod=6)  # FORCAST(EMA(CLOSE, 11), 6)
a4 = talib.LINEARREG(ema14, timeperiod=6)  # FORCAST(EMA(CLOSE, 14), 6)
a5 = talib.LINEARREG(ema17, timeperiod=6)  # FORCAST(EMA(CLOSE, 17), 6)

b = a1 + a2 + a3 + a4 - 4 * a5  # B := A1 + A2 + A3 + A4 - 4 * A5

towerc = talib.EMA(b, timeperiod=2)  # TOWERC := EMA(B, 2)
print(towerc)
# 根据条件筛选符合的股票代码
cond1 = towerc >= talib.SMA(towerc, timeperiod=1)  # TOWERC >= REF(TOWERC, 1)
cond2 = close < talib.SMA(close, timeperiod=talib.BARSLAST(cond1) + 1)  # CLOSE < REF(CLOSE, BARSLAST(COND1) + 1)
cond3 = towerc > talib.SMA(towerc, timeperiod=talib.BARSLAST(cond1) + 1)  # TOWERC > REF(TOWERC, BARSLAST(COND1) + 1)

# 符合所有条件的股票代码
selected_codes = df['code'][(cond1 & cond2 & cond3)].values

# 输出选中的股票代码
for code in selected_codes:
    print(code)