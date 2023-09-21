import sys
import traceback
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
from AkShare import AkShare
from Stock import Stock
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi
from strategy.LiuCaiShenLong import LiuCaiShenLong
from strategy.FaCaiXian import FaCaiXian

# 获取命令行参数（忽略第一个参数，即脚本文件名）
args = sys.argv[1:]

# 设置默认文件路径
filepath = "csv/A.csv"

# 如果有参数传递，则使用参数作为文件路径的一部分
if args:
    filepath = f"csv/{args[0]}"
    
df_a = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_a['code'].values

result = []
strategyName = []

for index, code in tqdm(enumerate(stock_codes), total=len(stock_codes), desc='Processing'):
    # 设置选股开始时间和结束时间
    start_date = '20210101'
    # end_date = '20230904'
    end_date = datetime.now().strftime("%Y%m%d")

    try:
        ak = AkShare(code, start_date, end_date)
        ak.get_stock_daily()
        # 实例化股票类
        stock = Stock(ak.df, ak.code)
        stock.debugger()

        # stock.use(DailyGoldenCross('日线金叉', ak.df, 3))
        # stock.use(HongLiBeiLiWang('弘历背离王', ak.df, 3))
        stock.use(HeiMa('黑马', ak.df, 1))
        # stock.use(JiuHouNiuYi('九牛转一', ak.df, 3))
        # stock.use(LiuCaiShenLong('六彩神龙', ak.df, 3))
        # stock.use(FaCaiXian('发财线', ak.df, 3))

    
        stock.exec()
        # 符合的策略百分比
        # percentage = stock.true_percentage()
        # print(f'执行 {code} 策略符合百分比为 {percentage}')

        # 是否可以买
        is_buy = stock.is_buy()
        if is_buy:
            print(f'{code} 符合策略结果')
            result.append(df_a.loc[index].tolist())
        # 存一下使用的策略名称
        strategyName = stock.getStrategyName()
    except Exception as e:
        traceback.print_exc()

if len(result) > 0:
    strategyName = '_'.join(strategyName)
    savepath = f'dist/{datetime.now()}_{strategyName}.txt';
    np.savetxt(savepath, result, delimiter=',', fmt='%s')
    print('选股结果保存成功！' + savepath)
else:
    print('未找到符合条件的股票，请调整你的策略！')


