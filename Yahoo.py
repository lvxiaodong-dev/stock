import retry
import yfinance as yf
import datetime as dt

class Yahoo:
    def __init__(self, code, start_date, end_date):
        # 股票代码
        self.code = code
        # 选股开始时间
        self.start_date = dt.datetime.strptime(start_date,'%Y%m%d')
        # 选股截止时间
        self.end_date = dt.datetime.strptime(end_date,'%Y%m%d')
        # 数据
        self.df = None

    # 失败重试3次
    #@retry.retry(exceptions=Exception, tries=3, delay=1)
    def get_stock_daily(self):
        self.df = yf.download(self.code, interval="1d", start=self.start_date, end=self.end_date)
        return self.df
    