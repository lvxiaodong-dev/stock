import libs.util as util
import traceback
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

class DataProvider:
    def __init__(self, DataApi):
        self.api = DataApi()

    # 下载股票信息数据
    def download_stock_info(self, stock_symbols, max_workers, callback):
        tasks = []
        for symbol in stock_symbols:
            tasks.append({
                'function': self.get_stock_info,
                'args': [symbol],
                'kwargs': {}
            })
        util.run_parallel_tasks(tasks, max_workers, '正在下载股票信息数据...', callback)

    # 下载股票历史日数据
    def download_stock_daily_data(self, stock_symbols, start_date, end_date, max_workers, callback):
        tasks = []
        for symbol in stock_symbols:
            tasks.append({
                'function': self.get_stock_daily_hist,
                'args': [symbol, self.api.format_daily_string(start_date), self.api.format_daily_string(end_date)],
                'kwargs': {}
            })

        util.run_parallel_tasks(tasks, max_workers, '正在下载日历史数据...', callback)

    # 下载股票历史分钟数据
    def download_stock_minute_hist(self, stock_symbols, start_date, end_date, period, max_workers, callback):
        tasks = []
        for symbol in stock_symbols:
            tasks.append({
                'function': self.get_stock_minute_hist,
                'args': [symbol, self.api.format_minute_string(start_date), self.api.format_minute_string(end_date), period],
                'kwargs': {}
            })
        def __callback(result):
            callback(result, period)
        util.run_parallel_tasks(tasks, max_workers, f'正在下载{period}分钟历史数据...', __callback)

    # 读取CSV文件内容
    def read_csv(self, csv_path):
        return self.api.read_csv(csv_path)
    
    # 格式化天时间
    def format_daily_string(self, date_string):
        return self.api.format_daily_string(date_string)
    
    # 格式化分钟时间
    def format_minute_string(self, date_string):
        return self.api.format_minute_string(date_string)
    
    # 获取股票信息
    def get_stock_info(self, *args):
        try:
            return self.api.get_stock_info(*args)
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"argument: {args}\n发生错误：{e}\n{error_traceback}")

    # 获取股票历史日数据
    def get_stock_daily_hist(self, *args):
        try:
            return self.api.get_stock_daily_hist(*args)
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"argument: {args}\n发生错误：{e}\n{error_traceback}")

    # 获取股票历史分钟数据
    def get_stock_minute_hist(self, *args):
        try:
            return self.api.get_stock_minute_hist(*args)
        except Exception as e:
            error_traceback = traceback.format_exc()
            logger.error(f"argument: {args}\n发生错误：{e}\n{error_traceback}")