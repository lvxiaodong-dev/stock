
import os
import numpy as np
from loguru import logger
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def run_parallel_tasks(tasks, max_workers, desc, callback):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for task in tasks:
            futures.append(executor.submit(task['function'], *task['args'], **task['kwargs']))
        for future in tqdm(futures, total=len(tasks), desc=desc):
            result = future.result()
            callback(result)

def save_array_with_directory(file_path, array):
    # 获取目录路径
    directory = os.path.dirname(file_path)
    
    # 如果目录不存在，创建目录
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # 保存数组到文件
    np.savetxt(file_path, array)

def log_error_with_time(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.error(f"{current_time} | {message}")