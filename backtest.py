import os, sys
import yaml
from loguru import logger
from screener.StockScreener import StockScreener
from data_provider.AkShare.AkShare import AkShare
from data_provider.Yahoo.Yahoo import Yahoo

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logger.remove() # 移除默认的处理器
logger.add(sys.stderr, level='INFO', format="{message}") # 新增一个往stderr输出的处理器,只输出INFO级别
logger.add("logs/backtest_errors.log", level="ERROR", format="{time:YYYY-MM-DD HH:mm:ss}\n{message}")


with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
class_obj = globals()[config['data_class']]
screener = StockScreener(class_obj)
screener.use("KDJ", "KDJ")
screener.run(backTest=True)

logger.info('Done!')