import sqlite3
import os, sys

# python check_db.py AAPL [DataProvider/Yahoo/Yahoo1.db]
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("check_db.py stock_code")
        sys.exit(0)

    print(f"checking db for {sys.argv[1]}")    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) > 2:
        dbfile=sys.argv[2]
    else:
        dbfile="data_provider/Yahoo/Yahoo.db"
    if not os.path.exists(dbfile):
        print(f"ERROR: {dbfile} does not exist")
        sys.exit(0)
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()
    # query_sql = '''
    #     SELECT * FROM stock_daily WHERE symbol = ? ORDER BY date DESC limit 10
    # '''
    # 执行查询语句
    # print(F"execting {query_sql}")
    #res = cursor.executemany(query_sql, (sys.argv[1]))
    print("**** stock_daily ****")
    res = cursor.execute(f'SELECT * FROM stock_daily WHERE symbol = "{sys.argv[1]}" ORDER BY date limit 1')
    result = res.fetchall()
    print(result)

    res = cursor.execute(f'SELECT * FROM stock_daily WHERE symbol = "{sys.argv[1]}" ORDER BY date DESC limit 1')
    result = res.fetchall()
    print(result)

    print("**** stock_weekly ****")
    res = cursor.execute(f'SELECT * FROM stock_weekly WHERE symbol = "{sys.argv[1]}" ORDER BY date limit 1')
    result = res.fetchall()
    print(result)

    res = cursor.execute(f'SELECT * FROM stock_weekly WHERE symbol = "{sys.argv[1]}" ORDER BY date DESC limit 1')
    result = res.fetchall()
    print(result)

    cursor.close()
    conn.close()
    