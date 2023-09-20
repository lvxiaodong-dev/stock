class StockDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def insert(self, stock):
        # 执行插入语句
    
    def query(self, code, start_date, end_date):
        # 执行查询语句并返回DataFrame
    
    def update(self, stock):
        # 执行更新语句