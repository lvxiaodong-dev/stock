import retry
import pandas as pd
import akshare as ak 
from datetime import datetime
from interfaces.DataApi import DataApi

class AkShare(DataApi):
    def __init__(self):
        pass

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def stock_individual_info_em(self, symbol):
        return ak.stock_individual_info_em(symbol=symbol, timeout=3)

    def get_stock_info(self, symbol):
        df = self.stock_individual_info_em(symbol)
        desired_keys = ['总市值', '流通市值', '总股本', '流通股', '行业']
        # 定义键的映射关系，将原键映射到新键
        key_mapping = {
            '总市值': 'MCAP',
            '流通市值': 'FCAP',
            '总股本': 'TOTSHR',
            '流通股': 'FLOSHR',
            '行业': 'INDUSTRY'
        }
        filtered_df = df[df['item'].isin(desired_keys)]
        data_dict = filtered_df.set_index('item').rename(index=key_mapping).T.to_dict('records')[0]
        data_dict['symbol'] = symbol
        return data_dict

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def stock_zh_a_hist(self, symbol, start_date, end_date):
        return ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date, period='daily', adjust="qfq", timeout=3)

    def get_stock_daily_hist(self, symbol, start_date, end_date):
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
                'AMOUNT': row['成交额'],
            }
            data_list.append(data_item)
        return data_list

    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def stock_zh_a_hist_min_em(self, symbol, start_date, end_date, period):
        return ak.stock_zh_a_hist_min_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust="qfq")

    def get_stock_minute_hist(self, symbol, start_date, end_date, period):
        df = self.stock_zh_a_hist_min_em(symbol, start_date, end_date, period)
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
        return csv_data['code'].values
    
    def format_daily_string(self, date):
        return date.strftime("%Y%m%d")
    
    def format_minute_string(self, date):
        return date.strftime("%Y-%m-%d %H:%M:%S")
    