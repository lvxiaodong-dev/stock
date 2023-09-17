import akshare as ak 

class Stock:
    def __init__(self, code, start_date, end_date):
        # 股票代码
        self.code = code
        # 选股开始时间
        self.start_date = start_date
        # 选股截止时间
        self.end_date = end_date
        # 股票数据
        self.df = None
        # 选股策略组
        self.strategyGroup = []
        # 选股结果
        self.result = []
        # 是否开启调试模式
        self.isDebugger = False

    def debugger(self, flag = True):
        self.isDebugger = flag

    def stock_zh_a_hist_daily(self):
        return ak.stock_zh_a_hist(symbol=self.code, start_date=self.start_date, end_date=self.end_date, period='daily', adjust="qfq")
    
    def stock_zh_a_hist_weekly(self):
        return ak.stock_zh_a_hist(symbol=self.code, start_date=self.start_date, end_date=self.end_date, period='weekly', adjust="qfq")
    
    def use(self, strategy):
        self.strategyGroup.append(strategy)

    def exec(self):
        for strategy in self.strategyGroup:
            flag = strategy.exec()
            self.result.append(flag)
            if self.isDebugger:
                print(f'{self.code}的{strategy.name}策略结果:{flag}')

    # 是否所有策略都符合条件
    def is_buy(self):
        return all(self.result)

    # 符合策略的百分比
    def true_percentage(self):
        true_count = sum(self.result)
        percentage = (true_count / len(self.result)) * 100
        return percentage
    
    # 获取指标名称
    def getStrategyName(self):
        return [strategy.name for strategy in self.strategyGroup]