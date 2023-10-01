import yaml
from screener.StockScreener import StockScreener
from DataProvider.A.AkShare import AkShare
from DataProvider.US.Yahoo import Yahoo
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.LiuCaiShenLongGreen import LiuCaiShenLongGreen
from strategy.FaCaiXian import FaCaiXian
from strategy.CrackBottom import CrackBottom
from strategy.EntrySignal import EntrySignal

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
STOCK_TYPE = config['use']
class_obj = globals()[config[STOCK_TYPE]['api_class_name']]
screener = StockScreener(STOCK_TYPE, class_obj)

# 设置选股策略
# screener.use(DailyGoldenCross('日线金叉', 3))
# screener.use(HongLiBeiLiWang('弘历背离王', 3))
# screener.use(HeiMa('黑马', 3))
# screener.use(JiuHouNiuYi('九牛转一', 3))
# screener.use(LiuCaiShenLongGreen('六彩神龙绿色', 3))
# screener.use(FaCaiXian('发财线', 3))
# screener.use(CrackBottom('破底', 1))
screener.use(EntrySignal('建仓信号', 1))
screener.debugger()
screener.run()