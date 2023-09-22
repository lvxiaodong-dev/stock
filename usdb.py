from datetime import datetime
from db.USStockDB import YahooStockDB

max_workers = 3
filepath = "csv/nasdaq.csv"
start_date = datetime.strptime('20190101','%Y%m%d')
end_date = datetime.strptime('20230919','%Y%m%d')


db = YahooStockDB()

# db.delete()

db.create()

db.create_index()

db.download(max_workers, filepath, start_date, end_date)
print('下载完成！')

db.close()
