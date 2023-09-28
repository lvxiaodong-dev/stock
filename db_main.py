from DataProvider.AkShare.AkShare import AkShare
from DataProvider.Yahoo.Yahoo import Yahoo
from DBScreener import DBScreener

STOCK_TYPE = 'US'
screener = DBScreener(STOCK_TYPE, Yahoo)

screener.debugger()
screener.run()
print('下载完成！')