import sys
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import akshare as ak 
import pandas as pd
from tqdm import tqdm

class StockDB:
    def __init__(self):
        self.conn = sqlite3.connect('db/stock.db')
        self.cursor = self.conn.cursor()

    def delete(self):
        # 删除表
        drop_table_sql = '''
            DROP TABLE IF EXISTS stock_daily
        '''
        self.cursor.execute(drop_table_sql)
        self.conn.commit()

    def create(self):
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS stock_daily 
            (id TEXT PRIMARY KEY, 
            code TEXT NOT NULL,
            date TEXT NOT NULL,  
            open FLOAT, 
            close FLOAT,
            high FLOAT,
            low FLOAT,
            UNIQUE (code, date)
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()


    def create_index(self):
        # 创建索引的 SQL 语句
        create_index_sql = '''
            CREATE INDEX IF NOT EXISTS idx_stock_daily_code_date ON stock_daily (code, date)
        '''

        # 执行创建索引的语句
        self.cursor.execute(create_index_sql)

        # 提交事务
        self.conn.commit()

    # def update(self):
    # 执行更新语句

    def download(self, max_workers, filepath, start_date, end_date):
    # 执行插入语句
        df_a = pd.read_csv(filepath, dtype=str, engine="python")
        stock_codes = df_a['code'].values

        with tqdm(total=len(stock_codes), desc='Downloading stocks') as pbar:
            with ThreadPoolExecutor(max_workers) as executor:
                futures = []
                for code in stock_codes:
                    future = executor.submit(self.download_stock, code, start_date, end_date)
                    future.add_done_callback(lambda p: pbar.update(1))
                    futures.append(future)
                # 等待所有任务完成
                for future in futures:
                    future.result()

    def download_stock(self, code, start_date, end_date):
        conn = sqlite3.connect('db/stock.db')
        cursor = conn.cursor()

        df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, period='daily', adjust="qfq")
        data_list = []
        # 插入数据的 SQL 语句
        insert_data_sql = '''
            INSERT OR IGNORE INTO stock_daily (code, date, open, high, low, close)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        # 将 DataFrame 中的数据写入数据库
        for index, row in df.iterrows():
            data_list.append((code, row['日期'], row['开盘'], row['最高'], row['最低'], row['收盘']))
            
        # 执行批量插入操作
        cursor.executemany(insert_data_sql, data_list)
        conn.commit()
    
    def query(self, code, start_date, end_date):
        # 执行查询语句并返回DataFrame
        query_sql = '''
            SELECT * FROM stock_daily
            WHERE code = ? AND date >= ? AND date <= ?
            ORDER BY date ASC
        '''
        # 执行查询语句
        self.cursor.execute(query_sql, (code, start_date, end_date))

        # 获取查询结果
        results = self.cursor.fetchall()
        df = pd.DataFrame(results, columns=[column[0] for column in self.cursor.description])
        new_columns = {'date': '日期', 'open': '开盘', 'close': '收盘', 'high': '最高', 'low': '最低'}
        df = df.rename(columns=new_columns)
        self.conn.commit()
        return df


    def close(self):
        self.cursor.close()
        self.conn.close()