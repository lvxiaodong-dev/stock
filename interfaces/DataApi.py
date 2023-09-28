from abc import ABC, abstractmethod

class DataApi(ABC):

    @abstractmethod
    def get_stock_daily_data(self, codes):
        pass

    @abstractmethod
    def get_stock_minute_data(self, codes):
        pass

    @abstractmethod
    def get_stock_info(self, codes):
        pass

    @abstractmethod
    def read_csv(self, csv_path):
        pass

    @abstractmethod
    def format_date_string(self, date):
        pass
    