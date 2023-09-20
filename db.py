import sys
import sqlite3
import akshare as ak 
import pandas as pd
from tqdm import tqdm
from StockDB import StockDB

db = StockDB()

# db.delete()

# db.create()

# db.download()

db.create_index()

db.close()