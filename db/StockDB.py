import sys
import sqlite3
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

class StockDB:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def delete(self):
        # 删除表
        drop_table_sql = '''
            DROP TABLE IF EXISTS {}
        '''.format(self.table_name)
        self.cursor.execute(drop_table_sql)
        self.conn.commit()

    def create(self):
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS {} 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            code TEXT NOT NULL,
            date DATETIME NOT NULL,  
            open FLOAT, 
            close FLOAT,
            high FLOAT,
            low FLOAT,
            UNIQUE (code, date)
        );
        '''.format(self.table_name)
        self.cursor.execute(create_table_sql)
        self.conn.commit()


    def create_index(self):
        # 创建索引的 SQL 语句
        create_index_sql = '''
            CREATE INDEX IF NOT EXISTS idx_stock_daily_code_date ON {} (code, date)
        '''.format(self.table_name)

        # 执行创建索引的语句
        self.cursor.execute(create_index_sql)

        # 提交事务
        self.conn.commit()

    # def update(self):
    # 执行更新语句

    def batch_insert(self, data_list):
        # 插入数据的 SQL 语句
        insert_data_sql = '''
            INSERT OR IGNORE INTO {} (code, date, open, high, low, close)
            VALUES (?, ?, ?, ?, ?, ?)
        '''.format(self.table_name)
            
        # 执行批量插入操作
        self.cursor.executemany(insert_data_sql, data_list)
        self.conn.commit()

    
    def query(self, code, start_date, end_date):
        # 执行查询语句并返回DataFrame
        query_sql = '''
            SELECT * FROM {}
            WHERE code = ? AND date BETWEEN ? AND ?
            ORDER BY date ASC
        '''.format(self.table_name)
        # 执行查询语句
        self.cursor.execute(query_sql, (code, start_date, end_date))

        # 获取查询结果
        results = self.cursor.fetchall()
        df = pd.DataFrame(results, columns=[column[0] for column in self.cursor.description])
        self.conn.commit()
        return df
    
    def max_date(self):
        query_sql = "SELECT MAX(date) FROM {}".format(self.table_name)
        self.cursor.execute(query_sql)
        max_date = self.cursor.fetchone()[0]
        return datetime.strptime(max_date, "%Y-%m-%d").strftime("%Y%m%d") if max_date else max_date

    def close(self):
        self.cursor.close()
        self.conn.close()