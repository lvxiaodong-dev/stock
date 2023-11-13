import pandas as pd
from db.Database import Database
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

db_path = 'data_provider/Yahoo/Yahoo.db'
table_name = 'stock_daily'
db = Database(db_path)
db.connect()

filepath = 'data_provider/Yahoo/Yahoo_downloaded.csv'
stock_codes = db.get_symbols(table_name, "symbol")
df = pd.DataFrame(stock_codes, columns=['Symbol'])
df.to_csv(filepath, index=False)

db.disconnect()