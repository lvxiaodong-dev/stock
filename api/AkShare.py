import retry
import akshare as ak 
from tqdm import tqdm

class AkShare:
    def __init__(self, stock_codes, start_date, end_date):
        self.stock_codes = stock_codes
        self.start_date = start_date
        self.end_date = end_date

    def download(self, db):
        stock_codes = self.stock_codes
        for code in tqdm(stock_codes, desc='Processing'):
            data = self.download_stock_data(code)
            db.executemany(data)
        
        # 失败重试3次
    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def stock_zh_a_hist(self, code, start_date, end_date):
        self.df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period='daily', adjust="qfq")
        return self.df
    
    def download_stock_data(self, code):
        df = self.stock_zh_a_hist(code, self.start_date, self.end_date)
        data_list = []
        # 将 DataFrame 中的数据写入数据库
        for index, row in df.iterrows():
            data_list.append((code, row['日期'].strftime("%Y-%m-%d"), row['开盘'], row['最高'], row['最低'], row['收盘']))
            
        return data_list
