import sys
import traceback
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
from AkShare import AkShare
from Stock import Stock
from StockDB import StockDB
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.FaCaiXian import FaCaiXian


result = []
strategyName = []
# 设置默认文件路径
filepath = "csv/CS.csv"
# 设置选股开始时间和结束时间
start_date = '20190101'
end_date = '20230904'
 # end_date = datetime.now().strftime("%Y%m%d")

# 获取命令行参数（忽略第一个参数，即脚本文件名）
args = sys.argv[1:]
# 如果有参数传递，则使用参数作为文件路径的一部分
if args:
    filepath = f"csv/{args[0]}"


def read_csv(filepath):
    return pd.read_csv(filepath, dtype=str, engine="python")

def forEach(csv_df):
    db = StockDB()
    stock_codes = csv_df['code'].values
    for index, code in tqdm(enumerate(stock_codes), total=len(stock_codes), desc='Processing'):
        try:
            df = db.query(code, start_date, end_date)
            
            # 实例化股票类
            stock = Stock(df, code)
            stock.debugger()

            stock.use(DailyGoldenCross('日线金叉', df, 3))
            # stock.use(HongLiBeiLiWang('弘历背离王', df, 3))
            # stock.use(HeiMa('黑马', df, 1))
            # stock.use(JiuHouNiuYi('九牛转一', df, 3))
            # stock.use(LiuCaiShenLong('六彩神龙', df, 3))
            # stock.use(FaCaiXian('发财线', df, 3))

        
            stock.exec()
            # 符合的策略百分比
            # percentage = stock.true_percentage()
            # print(f'执行 {code} 策略符合百分比为 {percentage}')

            # 是否可以买
            is_buy = stock.is_buy()
            if is_buy:
                print(f'{code} 符合策略结果')
                result.append(csv_df.loc[index].tolist())
            # 存一下使用的策略名称
            strategyName = stock.getStrategyName()
        except Exception as e:
            traceback.print_exc()

def alert():
    global strategyName
    if len(result) > 0:
        strategyName = '_'.join(strategyName)
        savepath = f'dist/{datetime.now()}_{strategyName}.txt';
        np.savetxt(savepath, result, delimiter=',', fmt='%s')
        print('选股结果保存成功！' + savepath)
    else:
        print('未找到符合条件的股票，请调整你的策略！')


def main():
    csv_df = read_csv(filepath)
    forEach(csv_df)
    alert()

main()