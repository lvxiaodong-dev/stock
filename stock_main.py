import os, sys
import yaml
from loguru import logger
from screener.StockScreener import StockScreener
from data_provider.AkShare.AkShare import AkShare
from data_provider.AkShare_A_ETF.AkShare_A_ETF import AkShare_A_ETF
from data_provider.Yahoo.Yahoo import Yahoo

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger.remove() # 移除默认的处理器
logger.add(sys.stderr, level='DEBUG', format="{message}") # 新增一个往stderr输出的处理器,只输出(INFO, DEBUG)级别
logger.add("logs/stock_errors.log", level="ERROR", format="{time:YYYY-MM-DD HH:mm:ss}\n{message}")

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
class_obj = globals()[config['data_class']]
screener = StockScreener(class_obj)

# 设置选股策略
# screener.use('DailyGoldenCross', '日线金叉', 1)
# screener.use('WeeklyGoldenCross', '周线金叉', 1)
# screener.use('MonthlyGoldenCross', '月线金叉', 1)
# screener.use('DailyMA', '日均线趋势', 1)
# screener.use('WeekMA', '周均线趋势', 1)
# screener.use('HongLiBeiLiWang', '弘历背离王', 3)
# screener.use("HPosition", "HPosition", 1)
# screener.use('HeiMa', '黑马', 3)
# screener.use('JiuHouNiuYi', '九牛转一', 1)
# screener.use('LiuCaiShenLong', '六彩神龙', 1)
# screener.use('LiuCaiShenLongGreen', '六彩神龙绿色', 1)
# screener.use('FaCaiXian', '发财线', 1)
# screener.use('QueKouJiuZhuan_JianCang', '缺口九转-建仓信号', 1)
# screener.use('GuBiDaoShu_JinChang', '顾比倒数-进场', 1)
# screener.use('QianKunXian', '乾坤线-进场', 1)
screener.use('QianKunXian2', '乾坤线-进场2', 1)
# screener.use('HongLi_JinChang', '弘历进场', 1)
screener.run()

logger.info('Done!')