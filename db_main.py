import sys
import yaml
from loguru import logger
from DataProvider.A.AkShare import AkShare
from DataProvider.US.Yahoo import Yahoo
from screener.DBScreener import DBScreener

logger.remove() # 移除默认的处理器
logger.add(sys.stderr, level='INFO', format="{message}") # 新增一个往stderr输出的处理器,只输出INFO级别
logger.add("logs/db_errors.log", level="ERROR", format="{message}")

# A股 或 美股
CONFIG_TYPE = 'config_A'
# CONFIG_TYPE = 'config_US'

with open('config.yaml') as f:
    config = yaml.safe_load(f)
class_obj = globals()[config[CONFIG_TYPE]['api_class_name']]
screener = DBScreener(CONFIG_TYPE, class_obj)

screener.run()
logger.info('下载完成！')
