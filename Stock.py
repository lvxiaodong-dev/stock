import akshare as ak 

class Stock:
    def __init__(self, df, code):
        # 股票数据
        self.df = df
        # 股票代码
        self.code = code
        # 选股策略组
        self.strategyGroup = []
        # 选股结果
        self.result = []
        # 是否开启调试模式
        self.isDebugger = False

    def debugger(self, flag = True):
        self.isDebugger = flag

    def use(self, strategy):
        self.strategyGroup.append(strategy)

    def exec(self):
        for strategy in self.strategyGroup:
            flag = strategy.exec()
            self.result.append(flag)


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