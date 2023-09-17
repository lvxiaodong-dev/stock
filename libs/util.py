from datetime import datetime, timedelta

"""
生成以指定日期为起点的一系列日期。

参数：
start_date (str): 起始日期，格式为"YYYYMMDD"。
num_days (int): 要生成的日期数量。

返回值：
list: 包含生成的日期的列表。

示例：
>>> start_date = "20230904"
>>> num_days = 3
>>> generate_dates(start_date, num_days)
['20230904', '20230903', '20230902']
"""
def generate_dates(start_date, num_days):
    date_format = "%Y%m%d"
    dates = []
    current_date = datetime.strptime(start_date, date_format)

    for _ in range(num_days):
        dates.append(current_date.strftime(date_format))
        current_date -= timedelta(days=1)

    return dates