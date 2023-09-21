import sys
import sqlite3
import akshare as ak 
import pandas as pd
from tqdm import tqdm
from StockDB import StockDB

max_workers = 10
filepath = "csv/A.csv"
start_date = '20190101'
end_date = '20230919'


db = StockDB()

db.delete()

db.create()

db.create_index()

db.download(max_workers, filepath, start_date, end_date)
print('下载完成！')

db.close()
