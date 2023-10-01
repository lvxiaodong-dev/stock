import yaml
from DataProvider.A.AkShare import AkShare
from DataProvider.US.Yahoo import Yahoo
from screener.DBScreener import DBScreener

with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
STOCK_TYPE = config['use']
class_obj = globals()[config[STOCK_TYPE]['api_class_name']]
screener = DBScreener(STOCK_TYPE, class_obj)

screener.debugger()
screener.run()
print('下载完成！')