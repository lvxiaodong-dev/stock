import sys
import yaml
from loguru import logger
from screener.StockScreener import StockScreener
from data_provider.AkShare.AkShare import AkShare
from data_provider.AkShare_A_ETF.AkShare_A_ETF import AkShare_A_ETF
from data_provider.Yahoo.Yahoo import Yahoo
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.LiuCaiShenLongGreen import LiuCaiShenLongGreen
from strategy.FaCaiXian import FaCaiXian
from strategy.QueKouJiuZhuan_JianCang import QueKouJiuZhuan_JianCang
from strategy.GuBiDaoShu_JinChang import GuBiDaoShu_JinChang
from strategy.QianKunXian import QianKunXian

logger.remove() # 移除默认的处理器
logger.add(sys.stderr, level='DEBUG', format="{message}") # 新增一个往stderr输出的处理器,只输出(INFO, DEBUG)级别
logger.add("logs/stock_errors.log", level="ERROR", format="{time:YYYY-MM-DD HH:mm:ss}\n{message}")

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
class_obj = globals()[config['data_class']]
screener = StockScreener(class_obj)

# 设置选股策略
# screener.use('DailyGoldenCross', '日线金叉', 1)
# screener.use('HongLiBeiLiWang', '弘历背离王', 3)
# screener.use('HeiMa', '黑马', 3)
# screener.use('JiuHouNiuYi', '九牛转一', 1)
# screener.use('LiuCaiShenLong', '六彩神龙', 1)
# screener.use('LiuCaiShenLongGreen', '六彩神龙绿色', 1)
# screener.use('FaCaiXian', '发财线', 1)
# screener.use('QueKouJiuZhuan_JianCang', '缺口九转-建仓信号', 1)
# screener.use('GuBiDaoShu_JinChang', '顾比倒数-进场', 1)
# screener.use('QianKunXian', '乾坤线-进场', 1)
screener.run()

logger.info('Done!')