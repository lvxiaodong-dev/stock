import pandas as pd
from datetime import datetime
from api.Yahoo import Yahoo
from db.StockDB import StockDB
#import csv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
db_path = 'db/stock.db'
table_name = 'stock_daily_us'

filepath = "csv/us_yahoo.csv"
#downloaded_filepath = F"csv/{os.path.basename(filepath)}_downloaded.csv"
df_csv = pd.read_csv(filepath, dtype=str, engine="python")
#df_csv = pd.DataFrame(["AAPL"], columns=['Symbol'])

stock_codes = df_csv['Symbol']

start_date = '20200101'
end_date = datetime.now().strftime("%Y%m%d")


db = StockDB(db_path, table_name)

db.delete()

db.create()

db.create_index()

max_date = db.max_date()
if max_date:
    start_date = max_date
    
api = Yahoo(stock_codes, start_date, end_date)
api.download(db)
db.close()

#fields = ["Symbol"]
#with open(downloaded_filepath, 'w') as f:
#    write = csv.writer(f)
#    write.writerow(fields)
#    write.writerows(api.downloaded_codes)

print('下载完成！')

