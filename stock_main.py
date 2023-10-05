import yaml
from screener.StockScreener import StockScreener
from DataProvider.A.AkShare import AkShare
from DataProvider.US.Yahoo import Yahoo
from strategy import *

import os,sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('config.yaml') as f:
    config = yaml.safe_load(f)

STOCK_TYPE = config['use']
class_obj = globals()[config[STOCK_TYPE]['api_class_name']]
screener = StockScreener(STOCK_TYPE, class_obj)

# 设置选股策略
# screener.use(DailyGoldenCross.DailyGoldenCross('日线金叉', 3))
# screener.use(HongLiBeiLiWang.HongLiBeiLiWang('弘历背离王', 3))
# screener.use(HeiMa.HeiMa('黑马', 3))
#screener.use(JiuHouNiuYi.JiuHouNiuYi('九牛转一', 2))
# screener.use(LiuCaiShenLongGreen.LiuCaiShenLongGreen('六彩神龙绿色', 3))
# screener.use(FaCaiXian.FaCaiXian('发财线', 3))
# screener.use(QueKouJiuZhuan_JianCang.QueKouJiuZhuan_JianCang('缺口九转-建仓信号', 2))
screener.use(GuBiDaoShu_JinChang.GuBiDaoShu_JinChang('顾比倒数-进场', 1))
screener.debugger()
screener.run()