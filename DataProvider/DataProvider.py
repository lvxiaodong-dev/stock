from tqdm import tqdm
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import libs.util as util

class DataProvider:
    def __init__(self, DataApi):
        self.api = DataApi()

    # 下载股票历史日数据
    def download_stock_daily_data(self, stock_symbols, start_date, end_date, max_workers, callback):
        tasks = []
        for symbol in stock_symbols:
            tasks.append({
                'function': self.api.get_stock_daily_hist,
                'args': [symbol, self.format_date_string(start_date), self.format_date_string(end_date)],
                'kwargs': {}
            })

        util.run_parallel_tasks(tasks, max_workers, callback)

    # 下载股票历史分钟数据
    def download_stock_minute_hist(self, stock_symbols, start_date, end_date, max_workers, callback):
        tasks = []
        for symbol in stock_symbols:
            tasks.append({
                'function': self.api.get_stock_minute_hist,
                'args': [symbol, start_date, end_date],
                'kwargs': {}
            })

        util.run_parallel_tasks(tasks, max_workers, callback)

    # 下载股票信息数据
    def download_stock_info(self, stock_symbols, start_date, end_date, max_workers, callback):
        tasks = []
        for symbol in stock_symbols:
            tasks.append({
                'function': self.api.get_stock_info,
                'args': [symbol, start_date, end_date],
                'kwargs': {}
            })

        util.run_parallel_tasks(tasks, max_workers, callback)

    # 读取CSV文件内容
    def read_csv(self, csv_path):
        return self.api.read_csv(csv_path)
    
    # 格式化时间
    def format_date_string(self, date_string):
        return self.api.format_date_string(date_string)