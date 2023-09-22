import pandas as pd
from datetime import datetime
from Stock import Stock
from db.AStockDB import AStockDB

from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.FaCaiXian import FaCaiXian

db = AStockDB()
filepath = 'csv/A.csv'
start_date = '20150101'
# end_date = '20230904'
end_date = datetime.now().strftime("%Y%m%d")

# 读csv文件获取stock_codes
csv_df = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = csv_df['code'].values

# 实例化股票类
stock = Stock(db, stock_codes)
# 设置选股日期
stock.set_date_range(start_date, end_date)

# 设置选股策略
# stock.use(DailyGoldenCross('日线金叉', 3))
# stock.use(HongLiBeiLiWang('弘历背离王', 3))
stock.use(HeiMa('黑马', 3))
# stock.use(JiuHouNiuYi('九牛转一', 3))
# stock.use(LiuCaiShenLong('六彩神龙', 1))
# stock.use(FaCaiXian('发财线', 3))

# 开启调试模式
# stock.debugger()

# 执行选股程序
stock.main()