import retry
import pandas as pd
import yfinance as yf
from datetime import datetime
from interfaces.DataApi import DataApi

class Yahoo(DataApi):
    def __init__(self):
        pass

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def yf_download(self, symbol, start_date, end_date):
        return yf.download(symbol, interval='1d', start=start_date, end=end_date, progress=False, timeout=3, threads=False)

    def get_stock_daily_hist(self, symbol, start_date, end_date):
        df = self.yf_download(symbol, start_date, end_date)
        data_list = []
        if df.empty:
            return data_list
        for index, row in df.iterrows():
            data_item = {
                'symbol': symbol,
                'date': index.strftime("%Y-%m-%d"),
                'OPEN': row['Open'],
                'CLOSE': row['Close'],
                'LOW': row['Low'],
                'HIGH': row['High'],
                'VOL': row['Volume'],
            }
            data_list.append(data_item)
        return data_list

    def get_stock_minute_hist(self, symbol, start_date, end_date, period):
        pass

    def get_stock_info(self, symbol):
        pass
    
    def read_csv(self, csv_path):
        csv_data = pd.read_csv(csv_path, dtype=str, engine="python")
        return csv_data['Symbol']
    
    def format_daily_string(self, date):
        return date
    