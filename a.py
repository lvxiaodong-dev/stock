import pandas as pd
from datetime import datetime
from src.StockAnalyzer import StockAnalyzer
from AkShare import AkShare

max_workers = 10
dbClass = AkShare
filepath = 'csv/A.csv'
start_date = '20190101'
# end_date = '20230904'
end_date = datetime.now().strftime("%Y%m%d")


csv_df = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = csv_df['code'].values

analyzer = StockAnalyzer(dbClass, stock_codes, start_date, end_date)

analyzer.analyze_stocks(max_workers)