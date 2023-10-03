import yaml
import traceback
import pandas as pd
from datetime import datetime
from DataProvider.DataProvider import DataProvider 
from db.Database import Database

class DBScreener:

    def __init__(self, STOCK_TYPE, DataApi):
        self.STOCK_TYPE = STOCK_TYPE
        self.provider = DataProvider(DataApi)
        self.config = self.read_config_yaml()
        # 是否开启调试模式
        self.isDebugger = False
    
    # 开启调试模式
    def debugger(self, flag = True):
        self.isDebugger = flag

    # 运行
    def run(self):
        try:
            self.download_daily()
        except Exception as e:
            if self.isDebugger:
                traceback.print_exc()
            else: 
                print(e);
    
    # 下载日数据
    def download_daily(self):
        self.db_path = self.config['db_path']
        self.db_stock_daily_table_name = self.config['db_stock_daily_table_name']
        self.csv_path = self.config['csv_path']
        self.start_date = self.config['start_date']
        self.end_date = self.config['end_date']
        self.today_as_end_date = self.config['today_as_end_date']
        # 使用当前日期做为结束时间
        if self.today_as_end_date:
            self.end_date = datetime.now().date()

        self.max_workers = self.config['max_workers']
        stock_symbols = self.provider.read_csv(self.csv_path)

        self.db = Database(self.db_path)
        self.db.connect()

        # self.db.drop_table(self.db_stock_daily_table_name)

        self.db.create_table(self.db_stock_daily_table_name, 'id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT NOT NULL, date DATETIME NOT NULL, OPEN FLOAT, CLOSE FLOAT, HIGH FLOAT, LOW FLOAT, VOL INTEGER, UNIQUE (symbol, date)')

        self.db.create_index(self.db_stock_daily_table_name, 'idx_stock_daily_code_date', 'symbol, date')

        # 查询最大时间，增量更新
        max_date = self.db.get_max_date(self.db_stock_daily_table_name, 'date')
        if max_date is not None:
            self.start_date = datetime.strptime(max_date, "%Y-%m-%d").date()

        self.provider.download_stock_daily_data(stock_symbols, self.start_date, self.end_date, self. max_workers, self.download_stock_daily_callback)
        self.db.disconnect()
        
    # 获取到数据之后，插入到本地数据库
    def download_stock_daily_callback(self, data_list):
        if len(data_list):
            self.db.insert_multiple_data(self.db_stock_daily_table_name, data_list)

    # 读配置文件
    def read_config_yaml(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            return config[self.STOCK_TYPE]
    
    # 读CSV文件
    def read_csv(self):
        return pd.read_csv(self.db_path, dtype=str, engine="python")