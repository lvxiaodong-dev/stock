from db.AStockDB import AStockDB

max_workers = 3
filepath = "csv/A.csv"
start_date = '20190101'
end_date = '20230919'


db = AStockDB()

db.delete()

db.create()

db.create_index()

db.download(max_workers, filepath, start_date, end_date)
print('下载完成！')

db.close()
