import retry
import pandas as pd
import akshare as ak 
from datetime import datetime
from interfaces.DataApi import DataApi

class AkShare_A_ETF(DataApi):
    def __init__(self):
        pass

    def get_stock_info(self, symbol):
        pass

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def fund_etf_hist_em(self, symbol, start_date, end_date, period):
        return ak.fund_etf_hist_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust="qfq")

    def get_stock_daily_hist(self, symbol, start_date, end_date, period):
        df = self.fund_etf_hist_em(symbol, start_date, end_date, period)
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
                'AMOUNT': row['成交额'],
            }
            data_list.append(data_item)
        return data_list

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def fund_etf_hist_min_em(self, symbol, start_date, end_date, period):
        return ak.fund_etf_hist_min_em(symbol=symbol, start_date=start_date, end_date=end_date, period=str(period), adjust='qfq')

    def get_stock_minute_hist(self, symbol, start_date, end_date, period):
        df = self.fund_etf_hist_min_em(symbol, start_date, end_date, period)
        data_list = []
        for index, row in df.iterrows():
            data_item = {
                'symbol': symbol,
                'date': row['时间'],
                'OPEN': row['开盘'],
                'CLOSE': row['收盘'],
                'LOW': row['最低'],
                'HIGH': row['最高'],
                'VOL': row['成交量'],
                'AMOUNT': row['成交额'],
            }
            data_list.append(data_item)
        return data_list

    def read_csv(self, csv_path):
        csv_data = pd.read_csv(csv_path, dtype=str, engine="python")
        return csv_data['symbol'].values
    
    def format_daily_string(self, date):
        return date.strftime("%Y%m%d")
    
    def format_minute_string(self, date):
        return date.strftime("%Y-%m-%d %H:%M:%S")
    