import pandas as pd
from datetime import datetime
from api.Yahoo import Yahoo
from db.StockDB import StockDB

db_path = 'db/stock.db'
table_name = 'stock_daily_us'

filepath = "csv/US.csv"
df_csv = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_csv['Symbol']


start_date = '2022-01-01'
end_date = datetime.now().strftime("%Y-%m-%d")


api = Yahoo(stock_codes, start_date, end_date)
db = StockDB(db_path, table_name)

db.delete()

db.create()

db.create_index()

api.download(db)

db.close()

print('下载完成！')

