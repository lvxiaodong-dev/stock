import pandas as pd
from datetime import datetime
from api.AkShare_zh import AkShareZh
from db.Database import Database

db_name = 'db/stock.db'
daily_table_name = 'stock_daily_a'
info_table_name = 'stock_info_a'
# table_name = 'stock_60_period_a'

filepath = "csv/a.csv"
df_csv = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_csv['code'].values

start_date = '20200101'
end_date = datetime.now().strftime("%Y%m%d")

db = Database(db_name)
db.connect()

# 删除表格
db.drop_table(daily_table_name)
db.drop_table(info_table_name)

# 创建表格
db.create_table(daily_table_name, 'id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL, date DATETIME NOT NULL, OPEN FLOAT, CLOSE FLOAT, HIGH FLOAT, LOW FLOAT, VOL INTEGER, UNIQUE (code, date)')
db.create_table(info_table_name, 'id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL, CAPITAL INTEGER, UNIQUE (code)')

# 创建索引
db.create_index(daily_table_name, 'idx_stock_daily_code_date', 'code, date')

# 查询最大时间，增量更新
max_date = db.get_max_date(daily_table_name, 'date')
if max_date is not None:
    start_date = max_date

api = AkShareZh(stock_codes, start_date, end_date)
def download_callback(data_list):
    db.insert_multiple_data(daily_table_name, data_list)

api.download(download_callback)

db.disconnect()

print('下载完成！')