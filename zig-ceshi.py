
import akshare as ak
from MyTT import EMA, REF, FORCAST, BARSLAST
from ZIG import ZIG
 
df = ak.stock_zh_a_hist(symbol='600257', start_date=20220101, end_date=20230913, period='daily', adjust="qfq")

AA = ZIG(df, 3, 0.05)
BB = REF(ZIG(df, 3, 0.05), 1)

print(AA)
print(BB)