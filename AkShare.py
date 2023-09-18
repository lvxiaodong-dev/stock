import retry
import akshare as ak 

class AkShare:
    def __init__(self, code, start_date, end_date):
        # 股票代码
        self.code = code
        # 选股开始时间
        self.start_date = start_date
        # 选股截止时间
        self.end_date = end_date
        # 数据
        self.df = None

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def stock_zh_a_hist_daily(self):
        self.df = ak.stock_zh_a_hist(symbol=self.code, start_date=self.start_date, end_date=self.end_date, period='daily', adjust="qfq")
        return self.df
    