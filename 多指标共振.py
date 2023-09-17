import traceback
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
from Stock import Stock
from strategy.DailyGoldenCross import DailyGoldenCross
from strategy.WeeklyGoldenCross import WeeklyGoldenCross
from strategy.HongLiBeiLiWang import HongLiBeiLiWang
from strategy.HeiMa import HeiMa
from strategy.JiuHouNiuYi import JiuHouNiuYi

filepath = "csv/A.csv"
df_a = pd.read_csv(filepath, dtype=str, engine="python")
stock_codes = df_a['code'].values

# 设置选股开始时间和结束时间
start_date = '20190101'
# end_date = '20230904'
end_date = datetime.now().strftime("%Y%m%d")

result = []
strategyName = []

for index, code in tqdm(enumerate(stock_codes), total=len(stock_codes), desc='Processing'):
    # 实例化股票类
    stock = Stock(code, start_date, end_date)
    stock.debugger()
    daily_df = stock.stock_zh_a_hist_daily()
    # weekly_df = stock.stock_zh_a_hist_weekly()

    # stock.use(DailyGoldenCross('日线金叉', daily_df))
    # stock.use(WeeklyGoldenCross('周线金叉', weekly_df))
    # stock.use(HongLiBeiLiWang('弘历背离王', daily_df))
    # stock.use(HeiMa('黑马', daily_df))
    # stock.use(JiuHouNiuYi('九牛转一', daily_df))

    try:
        stock.exec()
        # 符合的策略百分比
        percentage = stock.true_percentage()
        # print(f'执行 {code} 策略符合百分比为 {percentage}')
    except Exception as e:
        traceback.print_exc()

    # 是否可以买
    is_buy = stock.is_buy()
    if is_buy:
        print(f'{code} 符合策略结果')
        result.append(df_a.loc[index].tolist())

    strategyName = stock.getStrategyName()

if len(result) > 0:
    strategyName = '_'.join(strategyName)
    savepath = f'{end_date}_{strategyName}.txt';
    np.savetxt(savepath, result, delimiter=',', fmt='%s')
    print('选股结果保存成功！' + savepath)
else:
    print('未找到符合条件的股票，请调整你的策略！')


