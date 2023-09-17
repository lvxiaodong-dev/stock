import akshare as ak 

class AkShare:
    def __init__(self, code, start_date, end_date):
        # 股票代码
        self.code = code
        # 选股开始时间
        self.start_date = start_date
        # 选股截止时间
        self.end_date = end_date
        # 日数据
        self.daily_df = None
        # 周数据
        self.daily_df = None

    def stock_zh_a_hist_daily(self):
        self.daily_df = ak.stock_zh_a_hist(symbol=self.code, start_date=self.start_date, end_date=self.end_date, period='daily', adjust="qfq")
        return self.daily_df
    
    def stock_zh_a_hist_weekly(self):
        self.weekly_df = ak.stock_zh_a_hist(symbol=self.code, start_date=self.start_date, end_date=self.end_date, period='weekly', adjust="qfq")
        return self.weekly_df