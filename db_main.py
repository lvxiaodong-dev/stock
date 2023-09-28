from DataProvider.AkShare.AkShare import AkShare
# from DataProvider.Yahoo.Yahoo import Yahoo
from DBScreener import DBScreener

STOCK_TYPE = 'A'
screener = DBScreener(STOCK_TYPE, AkShare)

screener.run()