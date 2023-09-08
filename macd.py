import akshare as ak
import pandas as pd
import talib as ta
import datetime as dt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

start = dt.datetime(2018, 1, 1).strftime("%Y%m%d")
now = dt.datetime.now().strftime("%Y%m%d")

filepath="SZ.csv"
stocklist = pd.read_csv(filepath,dtype=str,engine="python")
stock_codes = stocklist['A股代码'].values

for code in stock_codes:
  
  # 获取日线数据
  stock_df = ak.stock_zh_a_hist(symbol=code,start_date=start,end_date=now,period="daily",adjust="qfq")
  # 计算日线MACD
  macd_diff, macd_dea, macd_bar = ta.MACD(stock_df['收盘'], fastperiod=12, slowperiod=26, signalperiod=9) 
  macd_diff = macd_diff.dropna()
  macd_dea = macd_dea.dropna()

  # 获取周线数据
  stock_wk_df = ak.stock_zh_a_hist(symbol=code,start_date=start,end_date=now,period="weekly")
  # 计算周线MACD 
  wk_macd_diff, wk_macd_dea, wk_macd_bar = ta.MACD(stock_wk_df['收盘'], fastperiod=26, slowperiod=52, signalperiod=13)
  wk_macd_diff = wk_macd_diff.dropna()
  wk_macd_dea = wk_macd_dea.dropna()

  # 判断金叉
  if macd_diff.iat[-1] > macd_dea.iat[-1] and wk_macd_diff.iat[-1] < wk_macd_dea.iat[-1]:
    print(code)
