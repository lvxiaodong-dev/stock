import retry
import yfinance as yf
import datetime as dt
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class Yahoo:
    def __init__(self, stock_codes, start_date, end_date):
        self.stock_codes = stock_codes
        self.start_date = start_date
        self.end_date = end_date
        #self.downloaded_codes = stock_codes.copy()

    def small_market_value(self,code):
        try:
            market_cap = yf.Ticker(code).fast_info.market_cap
            #print(stock, market_cap)
            if market_cap < 10000000000:
                #print(F"Skip {code} since its cap {market_cap} is small")
                return True
        except Exception as e:
            #print("ERROR: failed to get market_cap")
            pass
        return False

    def download(self, db):
        codes = self.stock_codes
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for code in codes:
                futures.append(executor.submit(self.download_stock_data, code))
            for future in tqdm(futures, total=len(codes), desc='Downloading'): 
                data = future.result()
                if data:
                    db.batch_insert(data)

        # for code in tqdm(codes, desc='Processing'):
        #     data = self.download_stock_data(code)
        #     if data:
        #         db.batch_insert(data)

    # 失败重试3次
    # @retry.retry(exceptions=Exception, tries=3, delay=1)
    def get_stock_data(self, code, start_date, end_date):
        try:
            if (self.small_market_value(code)):
                #self.downloaded_codes.remove(code)
                return pd.DataFrame()
            return yf.download(code, interval='1d', start=start_date, end=end_date, progress=False)
        except Exception as ex:
            #self.downloaded_codes.remove(code)
            print(str(ex))
            return pd.DataFrame()

    def download_stock_data(self, code):
        try:
            df = self.get_stock_data(code, dt.datetime.strptime(self.start_date,'%Y%m%d'), dt.datetime.strptime(self.end_date,'%Y%m%d'))
        except Exception as ex:
            print(str(ex))
            return None
        if df.empty:
            return None
        data_list = []
        # 将 DataFrame 中的数据写入数据库
        # index is the date; shall we use "Adj Close"
        for index, row in df.iterrows():
            data_list.append((code, index.strftime("%Y-%m-%d"), row['Open'], row['High'], row['Low'], row['Close'], row["Volume"]))
        return data_list