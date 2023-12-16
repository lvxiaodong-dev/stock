https://github.com/polakowo/vectorbt

import msvcrt

if name == 'main':
    if len(sys.argv) != 2:
        print('请拖入需要转换的文件')
        first_chr = msvcrt.getwch()
        try:
            get_input_file(first_chr)
        except FunctionTimedOut:
            File_name.strip('"')
    else:
        sys.argv[1]

f = open(File_name, 'r')
newf = open('tradingview.txt', 'w')
text = f.read()

| 大部分配置都放在了config.yaml文件中，没有A股或美股的概念了， 只有数据源的概念， 数据源是哪个股就获取对应股市的数据，实现统一的接口即可。


# Windows python 安装
不要装最新的。装3.10.x
https://discord.com/channels/898763842992095262/899105966358954074/1079616880496611421


# python环境变量配置
https://discord.com/channels/898763842992095262/964102962383306802/1153561966749687838

# python 模块安装
安装 pip install akshare mytt numpy pandas retry SQLite4 ta-lib tqdm yfinance loguru pyaml

打开命令行，比如
pip3 install pandas

talib 模块安装
https://openapi.futunn.com/futu-api-doc/quick/env.html 

##### 下载数据
1. 打开 config.yaml 文件， 修改其中的 data_class , 可选值如下:
* Akshare
* Yahoo

1. 下载数据到本地db数据库
```shell
python db_main.py
```
#### 选股程序
1. 打开 config.yaml 文件， 修改其中的 period, 可选值如下:
* weekly / daily / 60 / 30 / 5 / 1
* only daily tested for US stocks 
* db_stock_daily
* db_stock_120_minute
* db_stock_60_minute
* db_stock_30_minute
* db_stock_15_minute
* db_stock_5_minute
* db_stock_1_minute

2. 执行选股命令
```shell
python stock_main.py
```


#### 策略类
strategy目录下存放选股策略

#### 多策略共振
stock_main.py文件中, 通过 screener.use 同时使用多个策略选股， 以及最近 X 天符合条件。

# 回测
python backtest.py  （所有在 db中的股票回测结果）
or  python backtest.py AAPL  （单个股票回测结果）
生成回测结果csv. 你可以用excel 打开。

更新 backtest.py 使用新的stragtety , 可以加上多个策略

策略样本strategy/KDJ.py，目前只在KDJ超买超卖确认实现。
```
class KDJ(Strategy):
    def __init__(self, *args):
        super().__init__(*args)
    
    ......
    
    def transactions(self, df, info):
        J=self.JVal(df, info)
        Buy=CROSS(J, 0)
        Sell=CROSS(100, J)
        return Buy, Sell

```


#### 问与答

如果你看到有股票下载失败，改变config.yaml 如下：

把data_provider\Yahoo\Yahoo.csv 改名比如 Yahoo.csv.ori 
把data_provider\Yahoo\Failures.csv 改名为 Yahoo.csv; 并且 第一行 加 Symbol
config.yaml 中，比如db_stock_daily： drop_table: 0

再运行一次 db_main.py
删掉data_provider\Yahoo\Yahoo.csv
把原来的改名的data_provider\Yahoo\Yahoo.csv.ori 改回 Yahoo.csv
循环直到没有错误

如果只是少数股票不行，更简单弥补, 比如如果AAPL下载失败
```
config.yaml 中，比如db_stock_daily： drop_table: 0
python db_main.py AAPL


可以同时下载daily and weekly
config.yaml
db_stock_weekly:
    disabled:0
db_stock_daily:
    disabled:0
period: weekly 就是周线选股

```

#### Notes
如何实现获利盘COST、WINNER函数编写
https://bigquant.com/wiki/doc/costwinner-o9aYUY6Jwq
