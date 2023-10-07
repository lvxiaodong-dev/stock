import yaml
from DataProvider.A.AkShare import AkShare
from DataProvider.US.Yahoo import Yahoo
from screener.DBScreener import DBScreener

# A股 或 美股
# CONFIG_TYPE = 'config_A'
CONFIG_TYPE = 'config_US'

with open('config.yaml') as f:
    config = yaml.safe_load(f)
class_obj = globals()[config[CONFIG_TYPE]['api_class_name']]
screener = DBScreener(CONFIG_TYPE, class_obj)

screener.debugger()
screener.run()
print('下载完成！')