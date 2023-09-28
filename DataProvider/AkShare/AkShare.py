import retry
import pandas as pd
import akshare as ak 
from datetime import datetime
from interfaces.DataApi import DataApi

class AkShare(DataApi):
    def __init__(self):
        pass

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def stock_zh_a_hist(self, symbol, start_date, end_date):
        return ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date, period='daily', adjust="qfq")

    def get_stock_daily_data(self, symbol, start_date, end_date):
        df = self.stock_zh_a_hist(symbol, start_date, end_date)
        data_list = []
        for index, row in df.iterrows():
            data_item = {
                'symbol': symbol,
                'date': row['日期'],
                'OPEN': row['开盘'],
                'CLOSE': row['收盘'],
                'LOW': row['最低'],
                'HIGH': row['最高'],
                'VOL': row['成交量'],
            }
            data_list.append(data_item)
        return data_list
        return df

    def get_stock_minute_data(self, symbol, start_date, end_date, period):
        return ak.stock_zh_a_hist_min_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust="qfq")

    def get_stock_info(self, symbol):
        return ak.stock_individual_info_em(symbol=symbol)
    
    def read_csv(self, csv_path):
        csv_data = pd.read_csv(csv_path, dtype=str, engine="python")
        return csv_data['code'].values
    
    def format_date_string(self, date):
        return date.strftime("%Y%m%d")
    