import retry
import sqlite3
import akshare as ak 
import pandas as pd

conn = sqlite3.connect('db/stock.db')
cursor = conn.cursor()

class AkShare:
    def __init__(self, code, start_date, end_date):
        # 股票代码
        self.code = code
        # 选股开始时间
        self.start_date = start_date
        # 选股截止时间
        self.end_date = end_date
        # 数据
        self.df = None

    # 失败重试3次
    @retry.retry(exceptions=Exception, tries=3, delay=1)
    def get_stock_daily(self):
        self.df = ak.stock_zh_a_hist(symbol=self.code, start_date=self.start_date, end_date=self.end_date, period='daily', adjust="qfq")
        return self.df
    
    def get(self):
        # 查询数据的 SQL 语句
        query_sql = '''
            SELECT * FROM stock_daily
            WHERE code = ? AND date >= ? AND date <= ?
            ORDER BY date ASC
        '''

        # 查询参数
        code = self.code
        start_date = self.start_date
        end_date = self.end_date

        # 执行查询语句
        cursor.execute(query_sql, (code,start_date,end_date))

        # 获取查询结果
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])

        new_columns = {'date': '日期', 'open': '开盘', 'close': '收盘', 'high': '最高', 'low': '最低'}
        self.df = df.rename(columns=new_columns)

        return self.df
    