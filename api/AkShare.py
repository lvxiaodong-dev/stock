from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class AkShare:
    def __init__(self, stock_codes, start_date, end_date):
        self.stock_codes = stock_codes
        self.start_date = start_date
        self.end_date = end_date
        self.key_mapping = {
            '日期': 'date',
            '开盘': 'OPEN',
            '收盘': 'CLOSE',
            '最高': 'HIGH',
            '最低': 'LOW',
            '成交量': 'VOL'
        }

    def download(self, callback):
        codes = self.stock_codes
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for code in codes:
                futures.append(executor.submit(self.download_stock_data, code))
            
            for future in tqdm(futures, total=len(codes), desc='Downloading'): 
                data = future.result()
                callback(data)

    def download_stock_data(self, code):
        df = self.get_stock_data(code, self.start_date, self.end_date)
        return self.format_df(df, code)
    
    def format_df(self, df, code):
        data_list = []
        for index, row in df.iterrows():
            data_item = {
                'code': code,
                'date': row['日期'],
                'OPEN': row['开盘'],
                'CLOSE': row['收盘'],
                'LOW': row['最低'],
                'HIGH': row['最高'],
                'VOL': row['成交量'],
            }
            data_list.append(data_item)
        return data_list