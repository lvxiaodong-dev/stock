import sqlite3
import pandas as pd
from datetime import datetime
class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        print('connect...')
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def drop_table(self, table_name):
        # 删除表格
        print('drop_table...')
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()

    def create_table(self, table_name, columns):
        # 创建表格
        print('create_table...')
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.connection.commit()
    
    def create_index(self, table_name, index_name, columns):
        # 创建索引
        print('create_index...')
        self.cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns})")
        self.connection.commit()

    def insert_data(self, table_name, data):
        # 插入数据
        print('insert_data...')
        placeholders = ', '.join(['?'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        self.cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.connection.commit()

    def insert_multiple_data(self, table_name, data_list):
        # 批量插入数据
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?'] * len(data_list[0]))
        query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = [tuple(data.values()) for data in data_list]
        self.cursor.executemany(query, values)
        self.connection.commit()

    # def update_data(self, table_name, data, condition):
    #     # 更新数据
    #     set_values = ', '.join([f"{column} = ?" for column in data.keys()])
    #     values = tuple(data.values())
    #     self.cursor.execute(f"UPDATE {table_name} SET {set_values} WHERE {condition}", values)
    #     self.connection.commit()

    # def delete_data(self, table_name, condition):
    #     # 删除数据
    #     self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
    #     self.connection.commit()

    def fetch_data(self, table_name, columns='*', condition=None):
        # 检索数据
        if condition:
            self.cursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        else:
            self.cursor.execute(f"SELECT {columns} FROM {table_name}")
        # 获取查询结果
        results = self.cursor.fetchall()
        df = pd.DataFrame(results, columns=[column[0] for column in self.cursor.description])
        return df
    
    def get_max_date(self, table_name, date_column):
        # 获取最大日期
        query = f"SELECT MAX({date_column}) FROM {table_name}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        max_date = result[0]
        return max_date
    
    def get_symbols(self, table_name, symbol_column):
        query_sql = f"SELECT DISTINCT {symbol_column} FROM {table_name}"
        # 执行查询语句
        # print(F"execting {query_sql}")
        a = self.connection.execute(query_sql)

        # 获取查询结果
        results = [] 
        rs = a.fetchall()
        for item in rs:
            results.append(item[0])
        return results
