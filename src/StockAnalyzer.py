import traceback
import numpy as np
from datetime import datetime
from tqdm import tqdm
from .Stock import Stock
from concurrent.futures import ThreadPoolExecutor
from db.AStockDB import AStockDB
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.FaCaiXian import FaCaiXian

class StockAnalyzer:
    def __init__(self, dbClass, stock_codes, start_date, end_date):
        self.dbClass = dbClass
        self.stock_codes = stock_codes
        self.start_date = start_date
        self.end_date = end_date
        self.result = []
        self.strategyName = []

    def process_stock(self, code):
        try:
            db = self.dbClass(code, self.start_date, self.end_date)
            df = db.get_stock_daily()

            # 实例化股票类
            stock = Stock(df, code)
            stock.debugger()

            stock.use(DailyGoldenCross('日线金叉', df, 3))
            stock.use(HongLiBeiLiWang('弘历背离王', df, 3))
            # stock.use(HeiMa('黑马', df, 1))
            # stock.use(JiuHouNiuYi('九牛转一', df, 3))
            # stock.use(LiuCaiShenLong('六彩神龙', df, 3))
            # stock.use(FaCaiXian('发财线', df, 3))

            stock.exec()

            self.strategyName = stock.getStrategyName()
            # 是否可以买
            is_buy = stock.is_buy()
            if is_buy:
                print(f'{code} 符合策略结果')
                return code
        except Exception as e:
            traceback.print_exc()

    def print_stock(self):
        if len(self.result) > 0:
            strategyName = '_'.join(self.strategyName)
            savepath = f'dist/{datetime.now()}_{strategyName}.txt'
            np.savetxt(savepath, self.result, delimiter=',', fmt='%s')
            print('选股结果保存成功！' + savepath)
        else:
            print('未找到符合条件的股票，请调整你的策略！')

    def analyze_stocks(self, max_workers):
        with ThreadPoolExecutor(max_workers) as executor:
            futures = []
            for code in self.stock_codes:
                futures.append(executor.submit(self.process_stock, code))

            for future in tqdm(futures, total=len(futures), desc='Processing'):
                result_code = future.result()
                if result_code:
                    self.result.append(result_code[0])

        self.print_stock()