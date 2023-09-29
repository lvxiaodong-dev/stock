import akshare as ak 
import traceback
import numpy as np
from datetime import datetime
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


class Stock:
    def __init__(self, db, stock_codes, ):
        # 股票数据库
        self.db = db
        # 股票code数组
        self.stock_codes = stock_codes
        # 策略名称
        self.strategyName = []
        # 股票数据
        self.df = None
        # 选股策略组
        self.strategies = []
        # 选股结果
        self.selected_stocks = []
        # 是否开启调试模式
        self.isDebugger = False

    def set_date_range(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def debugger(self, flag = True):
        self.isDebugger = flag

    def use(self, strategy):
        self.strategies.append(strategy)

    def exec(self):
        condition = []
        for strategy in self.strategies:
            strategy.set_df(self.df)
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
    def find_stock(self, code):
        self.df = self.db.query(code, self.start_date, self.end_date)
        condition = self.exec()
        # 是否可以买
        is_buy = self.is_buy(condition)
        if is_buy:
            self.isDebugger and print(f'{code} 符合策略结果')
            self.selected_stocks.append(code)

    def print_stock(self):
        if len(self.selected_stocks) > 0:
            strategyName = '_'.join(self.getStrategyName())
            savepath = f'dist/{datetime.now()}_{strategyName}.txt'
            np.savetxt(savepath, self.selected_stocks, delimiter=',', fmt='%s')
            print('选股结果保存成功！' + savepath)
        else:
            print('未找到符合条件的股票，请调整你的策略！')

    def main(self):
        for code in tqdm(self.stock_codes, desc='Processing'):
            try:
                self.find_stock(code)
            except Exception as e:
                if self.isDebugger:
                     traceback.print_exc()
                else:
                    print(e)

        self.print_stock()