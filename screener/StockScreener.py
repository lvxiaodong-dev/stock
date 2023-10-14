import os,sys,importlib
import yaml
import traceback
import pandas as pd
import numpy as np
from loguru import logger
from datetime import datetime, timedelta
from tqdm import tqdm
from DataProvider.DataProvider import DataProvider 
from db.Database import Database

class StockScreener:

    def __init__(self, DataApi):
        self.provider = DataProvider(DataApi)
        self.config = self.read_config_yaml()
        # 策略名称
        self.strategyName = []
        # 选股策略组
        self.strategies = []
        # 选股结果
        self.selected_stocks = []

    # 运行程序
    def run(self):
        self.data_class = self.config['data_class']
        self.db_path = f'DataProvider/{self.data_class}/{self.data_class}.db'
        self.csv_path = f'DataProvider/{self.data_class}/{self.data_class}.csv'
        self.mode = self.config['mode']
        db_stock_config = self.config['db_tables'][self.mode]
        self.table_name = db_stock_config['table_name']
        self.start_date = db_stock_config['date_range']['start_date']
        self.end_date = db_stock_config['date_range']['end_date']
        self.today_as_end_date = db_stock_config['date_range']['today_as_end_date']
        self.recent_day = db_stock_config['date_range']['recent_day']
        today = datetime.now().date()
        # 使用当前日期做为结束时间
        if self.today_as_end_date:
            current_date = datetime.now().date()
            self.end_date = current_date
         # 最近recent_day天的数据
        if self.recent_day:
            self.start_date = today - timedelta(days=self.recent_day)
            self.end_date = today
        
        #self.stock_symbols = self.provider.read_csv(self.csv_path)
        self.db = Database(self.db_path)
        self.db.connect()
        if (len(sys.argv) < 2):
            self.stock_symbols=pd.Series(self.db.get_symbols(self.table_name, "symbol"))
        else:
            self.stock_symbols=pd.Series([sys.argv[1]])

        max_date = self.db.get_max_date(self.table_name, 'date')
        print(f"Searching stocks until {max_date}")
        self.main()

        self.db.disconnect()
    
    # 使用的策略
    def use(self, strategy):
        self.strategies.append(strategy)

    # 使用的策略
    def use(self, strategyName, description="", recent_day=1):
        if description == "":
            description = strategyName
        pkg = importlib.import_module(f"strategy.{strategyName}")
        #klass=globals()[f"{strategyName}.{strategyName}"]
        #klass=globals()[pkg[0]]
        klass = getattr(pkg, strategyName)
        self.strategies.append(klass(description, recent_day))

    # 执行选股
    def exec(self, df):
        condition = []
        for strategy in self.strategies:
            strategy.set_df(df)
            flag = strategy.exec()
            condition.append(flag)
        
        return condition
    
    # 是否所有策略都符合条件
    def is_buy(self, condition):
        return all(condition)
    
    # 获取指标名称
    def getStrategyName(self):
        return [strategy.name for strategy in self.strategies]
    
    # 找股票
    def find_stock(self, symbol):
        df = self.db.fetch_data(self.table_name, '*', "symbol = '{}' AND date >= '{}' AND date <= '{}' ORDER BY date ASC".format(symbol, self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d')))
        self.df = df
        if len(df) > 0:
            condition = self.exec(df)
            # 是否可以买
            is_buy = self.is_buy(condition)
            if is_buy:
                logger.debug(f'{symbol} 符合策略结果')
                self.selected_stocks.append(symbol)

    # 打印选股结果
    def print_stock(self):
        if len(self.selected_stocks) > 0:
            print('选股结果')
            print(self.selected_stocks)
            strategyName = '_'.join(self.getStrategyName())
            savepath = f'dist/{self.mode}/{datetime.now().strftime("%Y%m%d_%H%M%S")}_{strategyName}.txt'
            # 获取目录路径
            directory = os.path.dirname(savepath)
            
            # 如果目录不存在，创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            np.savetxt(savepath, self.selected_stocks, delimiter=',', fmt='%s')
            logger.info('选股结果保存成功！' + savepath)
        else:
            logger.info('未找到符合条件的股票，请调整你的策略！')

    # 主程序入口
    def main(self):
        for symbol in tqdm(self.stock_symbols, desc='Processing'):
            try:
                self.find_stock(symbol)
            except Exception as e:
                logger.error(f"argument: {symbol, self.start_date, self.end_date, self.mode}\n发生错误：{e}\n{traceback.format_exc()}")

        self.print_stock()

    # 读配置文件
    def read_config_yaml(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            return config
    
    # 读CSV文件
    def read_csv(self):
        return pd.read_csv(self.db_path, dtype=str, engine="python")