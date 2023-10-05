import os,sys
import yaml
import traceback
import pandas as pd
import numpy as np
import libs.util as util
from datetime import datetime
from tqdm import tqdm
from DataProvider.DataProvider import DataProvider 
from db.Database import Database

class StockScreener:

    def __init__(self, STOCK_TYPE, DataApi):
        self.STOCK_TYPE = STOCK_TYPE
        self.provider = DataProvider(DataApi)
        self.config = self.read_config_yaml()
        # 策略名称
        self.strategyName = []
        # 选股策略组
        self.strategies = []
        # 选股结果
        self.selected_stocks = []
         # 是否开启调试模式
        self.isDebugger = False

    # 运行程序
    def run(self):
        self.db_path = self.config['db_path']
        self.db_stock_daily_table_name = self.config['db_stock_daily_table_name']
        self.csv_path = self.config['csv_path']
        self.start_date = self.config['start_date']
        self.end_date = self.config['end_date']
        self.today_as_end_date = self.config['today_as_end_date']
        if self.today_as_end_date:
            current_date = datetime.now().date()
            self.end_date = current_date
        
        #self.stock_symbols = self.provider.read_csv(self.csv_path)
        self.db = Database(self.db_path)
        self.db.connect()
        if (len(sys.argv) < 2):
            self.stock_symbols=pd.Series(self.db.get_symbols(self.db_stock_daily_table_name, "symbol"))
        else:
            self.stock_symbols=pd.Series([sys.argv[1]])

        max_date = self.db.get_max_date(self.db_stock_daily_table_name, 'date')
        print(f"Searching stocks until {max_date}")
        self.main()

        self.db.disconnect()

        print('下载完成！')
    
    # 开启调试模式
    def debugger(self, flag = True):
        self.isDebugger = flag

    # 使用的策略
    def use(self, strategy):
        self.strategies.append(strategy)

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
        df = self.db.fetch_data(self.db_stock_daily_table_name, '*', "symbol = '{}' AND date >= '{}' AND date <= '{}' ORDER BY date ASC".format(symbol, self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d')))
        if len(df) > 0:
            date = datetime.strptime(df.iloc[-1]['date'], "%Y-%m-%d").date()
            # 时间不符合的不查询，停牌，节假日等情况
            if date <= self.end_date:
                condition = self.exec(df)
                # 是否可以买
                is_buy = self.is_buy(condition)
                if is_buy:
                    self.isDebugger and print(f'{symbol} 符合策略结果')
                    self.selected_stocks.append(symbol)

    # 打印选股结果
    def print_stock(self):
        if len(self.selected_stocks) > 0:
            strategyName = '_'.join(self.getStrategyName())
            savepath = f'dist/{datetime.now()}_{strategyName}.txt'
            # 获取目录路径
            directory = os.path.dirname(savepath)
            
            # 如果目录不存在，创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            np.savetxt(savepath, self.selected_stocks, delimiter=',', fmt='%s')
            print('选股结果保存成功！' + savepath)
        else:
            print('未找到符合条件的股票，请调整你的策略！')

    # 主程序入口
    def main(self):
        for symbol in tqdm(self.stock_symbols, desc='Processing'):
            try:
                self.find_stock(symbol)
            except Exception as e:
                print(f"Exception for {symbol}")
                if self.isDebugger:
                     traceback.print_exc()
                else: 
                    print(e)

        self.print_stock()

    # 读配置文件
    def read_config_yaml(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            return config[self.STOCK_TYPE]
    
    # 读CSV文件
    def read_csv(self):
        return pd.read_csv(self.db_path, dtype=str, engine="python")