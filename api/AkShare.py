from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class AkShare:
    def __init__(self, stock_codes, start_date, end_date):
        self.stock_codes = stock_codes
        self.start_date = start_date
        self.end_date = end_date

    def download(self, db):
        codes = self.stock_codes
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for code in codes:
                futures.append(executor.submit(self.download_stock_data, code))
            
            for future in tqdm(futures, total=len(codes), desc='Downloading'): 
                data = future.result()
                db.batch_insert(data)

    def download_stock_data(self, code):
        df = self.get_stock_data(code, self.start_date, self.end_date)
        data_list = []
        # 将 DataFrame 中的数据写入数据库
        for index, row in df.iterrows():
            data_list.append((code, self.getDate(row), row['开盘'], row['最高'], row['最低'], row['收盘'], row['成交量']))
        return data_list

    