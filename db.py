import sys
import sqlite3
import akshare as ak 
import pandas as pd
from tqdm import tqdm


conn = sqlite3.connect('db/stock.db')

cursor = conn.cursor()

# 删除表的 SQL 语句
drop_table_sql = '''
    DROP TABLE IF EXISTS stock_daily
'''
cursor.execute(drop_table_sql)


# 创建表格的 SQL 语句
create_table_sql = '''
    CREATE TABLE IF NOT EXISTS stock_info 
    (code INTEGER PRIMARY KEY, 
    name TEXT NOT NULL);
'''
cursor.execute(create_table_sql)
conn.commit()


# 创建表格的 SQL 语句
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
cursor.execute(create_table_sql)
conn.commit()

filepath = "csv/A.csv"
df_a = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_a['code'].values

for index, code in tqdm(enumerate(stock_codes), total=len(stock_codes), desc='Processing'):
    start_date = '20190101'
    end_date = '20230919'

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


# for code in stock_codes:
#     # 查询数据的 SQL 语句
#     query_sql = '''
#         SELECT * FROM stock_daily
#         WHERE code = ? AND date >= ? AND date <= ?
#         ORDER BY date ASC
#     '''

#     # 查询参数
#     code = code
#     start_date = "20190101"
#     end_date = "20230904"

#     # 执行查询语句
#     cursor.execute(query_sql, (code,start_date,end_date))

#     # 获取查询结果
#     results = cursor.fetchall()
#     print(results)

#     df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])

#     new_columns = {'date': '日期', 'open': '开盘', 'close': '收盘', 'high': '最高', 'low': '最低'}
#     df = df.rename(columns=new_columns)

#     print(df)

# # 关闭游标对象和数据库连接
cursor.close()
conn.close()


