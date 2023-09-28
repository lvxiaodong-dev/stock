import pandas as pd
from datetime import datetime
from Stock import Stock
from db.StockDB import StockDB

from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.FaCaiXian import FaCaiXian
from strategy.CrackBottom import CrackBottom
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
db_path = 'db/stock.db'
table_name = 'stock_daily_us'
db = StockDB(db_path, table_name)

start_date = '2020-01-01'
end_date = datetime.now().strftime("%Y-%m-%d")

stock_codes=db.codes()
# 实例化股票类
stock = Stock(db, pd.Series(stock_codes))
# 设置选股日期
stock.set_date_range(start_date, end_date)

# 设置选股策略
stock.use(DailyGoldenCross('日线金叉', 1))
# stock.use(HongLiBeiLiWang('弘历背离王', 3))
# stock.use(HeiMa('黑马', 3))
# stock.use(JiuHouNiuYi('九牛转一', 3))
# stock.use(LiuCaiShenLong('六彩神龙', 1))
# stock.use(FaCaiXian('发财线', 3))
# stock.use(CrackBottom('破底', 1))

# 开启调试模式
# stock.debugger()

# 执行选股程序
stock.main()
