import os,sys,importlib
import yaml
import traceback
import pandas as pd
import numpy as np
from loguru import logger
from datetime import datetime, timedelta
from tqdm import tqdm
from data_provider.DataProvider import DataProvider 
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
        self.isBuy = True
        self.backTest = False

    # 运行程序
    def run(self, backTest=False):
        if 'isBuy' in self.config:
            self.isBuy = self.config['isBuy'] == 1
        self.backTest = backTest
        self.data_class = self.config['data_class']
        if "db" in self.config:
            #for example, stock screen for my holding list; db might be different
            self.db_path = f'data_provider/{self.data_class}/{self.config["db"]}.db'
        else:
            self.db_path = f'data_provider/{self.data_class}/{self.data_class}.db'
        self.csv_path = f'data_provider/{self.data_class}/{self.data_class}.csv'
        #self.stock_symbols = self.provider.read_csv(self.csv_path)
        self.db = Database(self.db_path)
        self.db.connect()
        self.period = self.config['period']
        db_stock_config = self.config['db_tables'][f'db_stock_{self.period}']
        table_name = db_stock_config['table_name']
        if (len(sys.argv) < 2):
            self.stock_symbols=pd.Series(self.db.get_symbols(table_name, "symbol"))
        else:
            self.stock_symbols=pd.Series([sys.argv[1]])

        max_date = self.db.get_max_date(table_name, 'date')
        print(f"Searching stocks until {max_date}")
        self.main(stock_symbols=self.stock_symbols)

        self.db.disconnect()
    
    # 使用的策略
    def use(self, strategyName, description="", recent_day=1):
        if description == "":
            description = strategyName
        pkg = importlib.import_module(f"strategy.{strategyName}")
        klass = getattr(pkg, strategyName)
        self.strategies.append(klass(description, recent_day))

    # 执行选股
    def exec(self, **kwargs):
        condition = []
        buy = None
        sell = None
        for strategy in self.strategies:
            if self.backTest:
                b, s =strategy.transactions(**kwargs)
                if buy is None:
                    buy = b
                else:
                    buy = buy & b

                if sell is None:
                    sell = s
                else:
                    sell = sell & s
            else:
                if self.isBuy:
                    flag = strategy.exec(**kwargs)  
                else:
                    flag = strategy.execSell(**kwargs)
                condition.append(flag)

        if self.backTest:
            return buy, sell
        return condition
    
    # 是否所有策略都符合条件
    def is_meet(self, condition):
        return all(condition)
    
    # 获取指标名称
    def getStrategyName(self):
        return [strategy.name for strategy in self.strategies]
    
    def orderName(self):
        return "买" if self.isBuy else "卖"

    # backtest
    def doBackTest(self, symbol, df, info):
        buy, sell = self.exec(df=df, info=info)

        pos=0
        percentchange=[]
        CLOSE=df.CLOSE
        for i in range(buy.size):
            if buy[i]:
                if(pos==0):
                    bp=CLOSE.iloc[i]
                    pos=1
            elif (sell[i]):
                if(pos==1):
                    pos=0
                    sp=CLOSE.iloc[i]
                    pc=(sp/bp-1)*100
                    percentchange.append(pc)

        # if(pos==1 and not sell[-1]):
        #     pos=0
        #     sp=CLOSE.iloc[-1]
        #     #print("Selling now at "+str(sp))
        #     pc=(sp/bp-1)*100
        #     percentchange.append(pc)


        gains=0
        ng=0
        losses=0
        nl=0
        totalR=1

        for i in percentchange:
            if(i>0):
                gains+=i
                ng+=1
            else:
                losses+=i
                nl+=1
            totalR=totalR*((i/100)+1)

        totalR=round((totalR-1)*100,2)

        if(ng>0):
            avgGain=gains/ng
            maxR=str(max(percentchange))
        else:
            avgGain=0
            maxR="undefined"

        if(nl>0):
            avgLoss=losses/nl
            maxL=str(min(percentchange))
            ratio=str(-avgGain/avgLoss)
        else:
            avgLoss=0
            maxL="undefined"
            ratio="inf"

        if(ng>0 or nl>0):
            battingAvg=ng/(ng+nl)
        else:
            battingAvg=0

        return[symbol, str(ng+nl), str(battingAvg), str(ratio), str(avgGain), str(avgLoss),
                str(maxR), str(maxL), str(totalR)]

    # 找股票
    def find_stock(self, symbol, **kwargs):
        condition = self.exec(**kwargs)
        # 是否可以买或者卖
        is_meet = self.is_meet(condition)
        if is_meet:
            logger.debug(f'{symbol} 符合策略结果')
            self.selected_stocks.append(symbol)

    # 打印选股结果
    def print_stock(self):
        if len(self.selected_stocks) > 0:
            print(f'选股结果-{self.orderName()}')
            print(self.selected_stocks)
            strategyName = '_'.join(self.getStrategyName())
            savepath = f'dist/{self.period}/{datetime.now().strftime("%Y%m%d_%H%M%S")}_{strategyName}_{self.orderName()}.txt'
            # 获取目录路径
            directory = os.path.dirname(savepath)
            
            # 如果目录不存在，创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            np.savetxt(savepath, self.selected_stocks, delimiter=',', fmt='%s')
            logger.info('选股结果保存成功！' + savepath)
        else:
            logger.info('未找到符合条件的股票，请调整你的策略！')

    def print_backtest(self, data):
        if len(data) > 0:
            testDf = pd.DataFrame(data, columns=['Symbol','Trades', 'BattingAve','Gain/LossRatio', 'AverageGain', 
                                                 'AverageLoss', 'MaxReturn', 'MaxLoss', 'ReturnRatio'])
            strategyName = '_'.join(self.getStrategyName())
            savepath = f'dist/{self.period}/{datetime.now().strftime("%Y%m%d_%H%M%S")}_{strategyName}_backtest.csv'
            # 获取目录路径
            directory = os.path.dirname(savepath)
            
            # 如果目录不存在，创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)
            testDf.to_csv(savepath, index=False)
            logger.info('回测结果保存成功！' + savepath)
        else:
            logger.info('未找到回测结果')

    # 主程序入口
    def main(self, **kwargs):
        stock_symbols = kwargs['stock_symbols']
        #self.period = self.config['period']
        if self.backTest:
            data=[]
        for symbol in tqdm(stock_symbols, desc='Processing'):
            try:
                db_stock_config = self.config['db_tables'][f'db_stock_{self.period}']
                table_name = db_stock_config['table_name']
                start_date = db_stock_config['date_range']['start_date']
                end_date = db_stock_config['date_range']['end_date']
                today_as_end_date = db_stock_config['date_range']['today_as_end_date']
                recent_day = db_stock_config['date_range']['recent_day']
                today = datetime.now().date()
                # 使用当前日期做为结束时间
                if today_as_end_date:
                    current_date = datetime.now().date()
                    end_date = current_date
                # 最近recent_day天的数据
                if recent_day:
                    start_date = today - timedelta(days=recent_day)
                    end_date = today

                df = self.db.fetch_data(table_name, '*', "symbol = '{}' AND date >= '{}' AND date <= '{}' ORDER BY date ASC".format(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                #info = self.db.fetch_firstrow_data('stock_info', '*', "symbol = '{}'".format(symbol))
                info = None
                if self.backTest:
                    data.append(self.doBackTest(symbol, df=df, info=info))
                else:
                    self.find_stock(symbol, df=df, info=info)
            except Exception as e:
                logger.error(f"argument: {symbol}\n发生错误：{e}\n{traceback.format_exc()}")
        if self.backTest:
            self.print_backtest(data)
        else:
            self.print_stock()

    # 读配置文件
    def read_config_yaml(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            return config
    
    # 读CSV文件
    def read_csv(self):
        return pd.read_csv(self.db_path, dtype=str, engine="python")