import akshare as ak
import pandas as pd
import numpy as np


# 股票代码列表
codes = []
with open('弘历背离王_daily_20230829.txt','r') as f:
    data = f.read()
    df = pd.DataFrame([line.split(',') for line in data.split('\n')]) 
    codes = df[0].values

# 设置持有期
start_date = '20230829'  
end_date = '20230911'

# 初始化存储每只股票的持有期回报率
returns = []

# 遍历处理每个股票
for code in codes:
    try:
        # 获取股票数据
        df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date)
        
        # 计算持有期收益率
        start_price = df.iloc[0]['收盘']
        end_price = df.iloc[-1]['收盘']
        holding_return = (end_price - start_price) / start_price * 100
        
        # 添加到列表
        returns.append(holding_return)
    except Exception as e:
        returns.append(0)


# 将持有期收益率转为DataFrame    
returns_df = pd.DataFrame({'code': codes, 'holding_return (%)': returns})

# 输出每只股票的持有期收益率 
print(returns_df)

#  平均收益率
average_return = np.mean(returns_df['holding_return (%)']) 
print("平均收益率: %.2f%%" % average_return)

# 计算总体平均胜率
win_rate = len(returns_df[returns_df['holding_return (%)'] > 0]) / len(returns_df) * 100

print("总体平均胜率: %.2f%%" % win_rate)