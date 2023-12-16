import retry
import warnings
import pandas as pd
import yfinance as yf
import os
from interfaces.DataApi import DataApi
from libs.MyTA import MyTA as mta

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
        #if (mta.small_market_value(symbol)):
        #    return pd.DataFrame()
        try:
            return yf.download(symbol, interval=interval, start=start_date, end=end_date, progress=False, timeout=3, threads=False)
        except Exception as ex:
            print(f"Downloading {symbol} Failed: {str(ex)}")
            return pd.DataFrame()

    def get_stock_daily_hist(self, symbol, start_date, end_date):
        df = self.yf_download(symbol, '1d', pd.Timestamp(start_date), pd.Timestamp(end_date))
        data_list = []
        if df.empty:
            failureFile=f"{os.path.dirname(os.path.abspath(__file__))}/failures.csv"
            print(f"ERROR: failed to download {symbol}")
            with open(failureFile,'a') as fh:
                fh.write(f"{symbol}\n")
            return data_list
        # if mta.small_volume(df):
        #     print(f"INFO: skip {symbol} due to small volume")
        #     return data_list
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
        df = self.yf_download(symbol, f'{period}m',pd.Timestamp(start_date), pd.Timestamp(end_date))
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