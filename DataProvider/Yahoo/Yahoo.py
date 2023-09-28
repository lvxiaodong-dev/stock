from interfaces.DataApi import DataApi
import yfinance as yf

class Yahoo(DataApi):
    def __init__(self):
        pass

    def get_stock_daily_data(self, symbol, start_date, end_date, period):
        return yf.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date, period='daily', adjust="qfq")

    def get_stock_minute_data(self, symbol, start_date, end_date, period):
        return yf.stock_zh_a_hist_min_em(symbol=symbol, start_date=start_date, end_date=end_date, period=period, adjust="qfq")

    def get_stock_info(self, symbol):
        return yf.stock_individual_info_em(symbol=symbol)
    