import retry
import akshare as ak 
from api.AkShare import AkShare

class AkShareZh(AkShare):
    def __init__(self, *args):
        super().__init__(*args)
        
    # 失败重试3次
    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def get_stock_data(self, code, start_date, end_date):
        self.df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period='daily', adjust="qfq")
        return self.df
    
    def getDate(self, row):
        return row['日期'].strftime("%Y-%m-%d")
