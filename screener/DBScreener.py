import yaml
import pandas as pd
from loguru import logger
from datetime import datetime, timedelta
from data_provider.DataProvider import DataProvider 
from db.Database import Database

class DBScreener:

    def __init__(self, DataApi):
        self.provider = DataProvider(DataApi)
        self.config = self.read_config_yaml()
    
    # 运行
    def run(self):
        self.data_class = self.config['data_class']
        self.db_path = f'data_provider/{self.data_class}/{self.data_class}.db'
        self.csv_path = f'data_provider/{self.data_class}/{self.data_class}.csv'
        self.max_workers = self.config['max_workers']
        self.stock_symbols = self.provider.read_csv(self.csv_path)
        logger.info('打开数据库连接')
        self.db = Database(self.db_path)
        self.db.connect()
        self.download_stock_info()
        self.download_daily('monthly')
        self.download_daily('weekly')
        self.download_daily('daily')
        self.download_minute('120')
        self.download_minute('60')
        self.download_minute('30')
        self.download_minute('15')
        self.download_minute('5')
        self.download_minute('1')
        logger.info('关闭数据库连接')
        self.db.disconnect()

    # 下载股票信息
    def download_stock_info(self):
        db_stock_config = self.config['db_tables']['db_stock_info']
        if db_stock_config['disabled']:
            return
        table_name = db_stock_config['table_name']
        ### 股票信息数据
        if db_stock_config['drop_table']:
            logger.info('删除股票信息表...')
            self.db.drop_table(table_name)
        logger.info('创建股票信息数据表...')
        self.db.create_table(table_name, 'id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT NOT NULL, MCAP FLOAT, FCAP FLOAT, TOTSHR FLOAT, FLOSHR FLOAT, INDUSTRY TEXT, UNIQUE (symbol)')
        logger.info('创建股票信息数据表索引...')
        self.db.create_index(table_name, 'idx_stock_daily_symbol', 'symbol')
        self.provider.download_stock_info(self.stock_symbols, self.max_workers, self.download_stock_info_callback)
        
    def download_stock_info_callback(self, data_dict):
        table_name = self.config['db_tables']['db_stock_info']['table_name']
        self.db.insert_data(table_name, data_dict)
    
    # 下载日数据
    def download_daily(self, period):
        db_stock_config = self.config['db_tables'][f'db_stock_{period}']
        if db_stock_config['disabled']:
            return
        table_name = db_stock_config['table_name']
        start_date = db_stock_config['date_range']['start_date']
        end_date = db_stock_config['date_range']['end_date']
        today_as_end_date = db_stock_config['date_range']['today_as_end_date']
        recent_day = db_stock_config['date_range']['recent_day']
        today = datetime.now().date()
        # 使用当前日期做为结束时间
        if today_as_end_date:
            end_date = today
        # 最近recent_day天的数据
        if recent_day:
            start_date = today - timedelta(days=recent_day)
            end_date = today

        ### 日历史数据
        if db_stock_config['drop_table']:
            logger.info(f'删除历史{period}数据表...')
            self.db.drop_table(table_name)
        logger.info(f'创建历史{period}数据表...')
        self.db.create_table(table_name, 'id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT NOT NULL, date DATETIME NOT NULL, OPEN FLOAT, CLOSE FLOAT, HIGH FLOAT, LOW FLOAT, VOL INTEGER, AMOUNT INTEGER, UNIQUE (symbol, date)')
        self.db.create_index(table_name, 'idx_stock_daily_symbol_date', 'symbol, date')
        # 查询最大时间，增量更新
        max_date = self.db.get_max_date(table_name, 'date')
        if max_date is not None:
            start_date = datetime.strptime(max_date, "%Y-%m-%d").date()
        self.provider.download_stock_daily_data(self.stock_symbols, start_date, end_date, period, self.max_workers, self.download_stock_daily_callback)
        
    # 获取到数据之后，插入到本地数据库
    def download_stock_daily_callback(self, data_list, period):
        table_name = self.config['db_tables'][f'db_stock_{period}']['table_name']
        if len(data_list):
            self.db.insert_multiple_data(table_name, data_list)

    # 下载30分钟历史数据
    def download_minute(self, period):
        db_stock_config = self.config['db_tables'][f'db_stock_{period}']
        if db_stock_config['disabled']:
            return
        table_name = db_stock_config['table_name']
        start_date = db_stock_config['date_range']['start_date']
        end_date = db_stock_config['date_range']['end_date']
        today_as_end_date = db_stock_config['date_range']['today_as_end_date']
        recent_day = db_stock_config['date_range']['recent_day']
        today = datetime.now()
        # 使用当前日期做为结束时间
        if today_as_end_date:
            end_date = today
        # 最近recent_day天的数据
        if recent_day:
            start_date = today - timedelta(days=recent_day)
            end_date = today
        ### 日历史数据
        if db_stock_config['drop_table']:
            logger.info(f'删除历史{period}分钟数据表...')
            self.db.drop_table(table_name)
        logger.info(f'创建历史{period}分钟数据表...')
        self.db.create_table(table_name, 'id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT NOT NULL, date DATETIME NOT NULL, OPEN FLOAT, CLOSE FLOAT, HIGH FLOAT, LOW FLOAT, VOL INTEGER, AMOUNT INTEGER, UNIQUE (symbol, date)')
        self.db.create_index(table_name, 'idx_stock_minute_symbol_date', 'symbol, date')
        # 查询最大时间，增量更新
        max_date = self.db.get_max_date(table_name, 'date')
        if max_date is not None:
            start_date = datetime.strptime(max_date, "%Y-%m-%d %H:%M:%S")
        self.provider.download_stock_minute_hist(self.stock_symbols, start_date, end_date, period, self.max_workers, self.download_stock_minute_callback)
        
    # 获取到数据之后，插入到本地数据库
    def download_stock_minute_callback(self, data_list, period):
        table_name = self.config['db_tables'][f'db_stock_{period}']['table_name']
        if len(data_list):
            self.db.insert_multiple_data(table_name, data_list)

    # 读配置文件
    def read_config_yaml(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            return config
    
    # 读CSV文件
    def read_csv(self):
        return pd.read_csv(self.db_path, dtype=str, engine="python")