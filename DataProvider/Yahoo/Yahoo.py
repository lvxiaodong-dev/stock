import retry
import warnings
import pandas as pd
import yfinance as yf
from datetime import datetime
from interfaces.DataApi import DataApi

warnings.filterwarnings("ignore", category=FutureWarning) 

class Yahoo(DataApi):
    def __init__(self):
        pass

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def get_stock_info(self, symbol):
        df = yf.Ticker(symbol)
        info = df.info
        float_shares = info.get('floatShares')
        current_price = info.get('currentPrice')

        if float_shares is not None and current_price is not None:
            fcap = float_shares * current_price
        else:
            fcap = None

        data_dict = {
            'symbol': symbol,
            'MCAP': info.get('marketCap', None),
            'FCAP': fcap,
            'TOTSHR': info.get('sharesOutstanding', None),
            'FLOSHR': info.get('floatShares', None),
            'INDUSTRY': info.get('industry', None),
        }
        return data_dict

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def yf_download(self, symbol, interval, start_date, end_date):
        return yf.download(symbol, interval=interval, start=start_date, end=end_date, progress=False, timeout=3, threads=False)

    def get_stock_daily_hist(self, symbol, start_date, end_date):
        df = self.yf_download(symbol, '1d', start_date, end_date)
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
        df = self.yf_download(symbol, f'{period}m',start_date, end_date)
        data_list = []
        if df.empty:
            return data_list
        for index, row in df.iterrows():
            data_item = {
                'symbol': symbol,
                'date': index.strftime("%Y-%m-%d %H:%M:%S"),
                'OPEN': row['Open'],
                'CLOSE': row['Close'],
                'LOW': row['Low'],
                'HIGH': row['High'],
                'VOL': row['Volume'],
            }
            data_list.append(data_item)
        return data_list
    
    def read_csv(self, csv_path):
        csv_data = pd.read_csv(csv_path, dtype=str, engine="python")
        return csv_data['Symbol']
    
    def format_daily_string(self, date):
        return date
    
    def format_minute_string(self, date):
        return date