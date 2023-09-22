import sys
import sqlite3
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

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
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
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
        stock_codes = self.read_csv(filepath)

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
        

    def download_stock(self):
        print('download_stock')
    
    def query(self):
        print('query')


    def close(self):
        self.cursor.close()
        self.conn.close()