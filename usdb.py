import pandas as pd
from datetime import datetime
from api.AkShare_us import AkShareUs
from db.StockDB import StockDB

db_path = 'db/stock.db'
table_name = 'stock_daily_us'

filepath = "csv/us.csv"
df_csv = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_csv['代码']

start_date = '20200101'
end_date = datetime.now().strftime("%Y%m%d")

db = StockDB(db_path, table_name)

# db.delete()

db.create()

db.create_index()

max_date = db.max_date()
if max_date:
    start_date = max_date

api = AkShareUs(stock_codes, start_date, end_date)
api.download(db)

db.close()

print('下载完成！')