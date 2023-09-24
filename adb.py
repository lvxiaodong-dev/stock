import pandas as pd
from datetime import datetime
from api.AkShare import AkShare
from db.StockDB import StockDB

db_path = 'db/stock.db'
table_name = 'stock_daily_a'
# table_name = 'stock_60_period_a'

filepath = "csv/A.csv"
df_csv = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_csv['code'].values

start_date = '20200101'
end_date = datetime.now().strftime("%Y%m%d")

db = StockDB(db_path, table_name)

# db.delete()

db.create()

db.create_index()

max_date = db.max_date()
if max_date:
    start_date = max_date

api = AkShare(stock_codes, start_date, end_date)
api.download(db)

db.close()

print('下载完成！')