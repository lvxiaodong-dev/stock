import retry
import pandas as pd
import yfinance as yf
from datetime import datetime
from interfaces.DataApi import DataApi

class Yahoo(DataApi):
    def __init__(self):
        pass

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

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def yf_download(self, symbol, start_date, end_date):
        #if (self.small_market_value(symbol)):
        #    return pd.DataFrame()
        try:
            return yf.download(symbol, interval='1d', start=start_date, end=end_date, progress=False, timeout=3, threads=False)
        except Exception as ex:
            print(f"Downloading {symbol} Failed: {str(ex)}")
            return pd.DataFrame()

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
    
    def format_date_string(self, date):
        return date
