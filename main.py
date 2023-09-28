from StockScreener import StockScreener
from DataProvider.AkShare.AkShare import AkShare
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.LiuCaiShenLongGreen import LiuCaiShenLongGreen
from strategy.FaCaiXian import FaCaiXian
from strategy.CrackBottom import CrackBottom

STOCK_TYPE = 'A'
screener = StockScreener(STOCK_TYPE, AkShare)

# 设置选股策略
screener.use(DailyGoldenCross('日线金叉', 3))
# screener.use(HongLiBeiLiWang('弘历背离王', 3))
# screener.use(HeiMa('黑马', 3))
# screener.use(JiuHouNiuYi('九牛转一', 3))
# screener.use(LiuCaiShenLongGreen('六彩神龙绿色', 3))
# screener.use(FaCaiXian('发财线', 3))
# screener.use(CrackBottom('破底', 1))
screener.debugger()
screener.run()