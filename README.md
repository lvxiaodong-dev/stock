| 大部分配置都放在了config.yaml文件中，没有A股或美股的概念了， 只有数据源的概念， 数据源是哪个股就获取对应股市的数据，实现统一的接口即可。

##### 安装依赖
1. 安装 python3
2. 安装 pip install akshare mytt numpy pandas retry ta-lib tqdm yfinance loguru pyyaml

##### 下载数据
1. 打开 config.yaml 文件， 修改其中的 data_class , 可选值如下:
* Akshare
* Yahoo

2. 执行下载命令
```shell
python db_main.py
```

#### 选股程序
1. 打开 config.yaml 文件， 修改其中的 mode, 可选值如下:
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
