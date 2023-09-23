import retry
import yfinance as yf
from tqdm import tqdm

class Yahoo:
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
    def get_stock_data(self, code, start_date, end_date):
        return yf.download(code, interval="1d", start=start_date, end=end_date, progress=False)
    
    def download_stock_data(self, code):
        df = self.get_stock_data(code, self.start_date, self.end_date)
        data_list = []
        # 将 DataFrame 中的数据写入数据库
        for index, row in df.iterrows():
            data_list.append((code, index.strftime("%Y-%m-%d"), row['Open'], row['High'], row['Low'], row['Close']))
            
        return data_list