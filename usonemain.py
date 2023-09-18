import pandas as pd
import datetime as dt
import yfinance as yf
import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from strategy.HeiMa import HeiMa

#成交额
def small_volume(df):
    try:
        last_volume = df['Volume'].iloc[-1]
        last_close = df['Close'].iloc[-1]
        last_dollar_volume = last_volume * last_close
        if last_dollar_volume < 10000:
            return True
    except Exception as e:
            pass
    return False

def small_market_value(code):
    try:
        market_cap = yf.Ticker(code).fast_info.market_cap
        #print(stock, market_cap)
        if market_cap < 1000000000:
            #print(F"Skip {code} since its cap {market_cap} is small")
            return True
    except Exception as e:
        #print("ERROR: failed to get market_cap")
        pass
    return False

# Get the CSV file name from the user
root = Tk()
root.withdraw()
csvfilename = askopenfilename(title="Select CSV File")
root.destroy()

# Load the stock symbols from the CSV file
stocklist = pd.read_csv(csvfilename, engine="python", encoding="ISO-8859-1")

# Set up yfinance
yf.pdr_override()
start = dt.datetime.now() - dt.timedelta(days=300)
now = dt.datetime.now()

result = []

# Iterate through each stock in the list
for i in range(len(stocklist)):
    stock = stocklist.iloc[i]["Symbol"]
    print(f"{i+1}/{len(stocklist)} {stock}")
    
    # Retrieve stock data from Yahoo Finance
    try:
        df = yf.download(stock, start, now)
    except Exception as e:
        print(f"Error retrieving data for {stock}:{str(e)}")
        continue

    if small_volume(df):
        continue
    if small_market_value(stock):
        continue

    algo=HeiMa('黑马', df, 1)
    try:
        if algo.find():
            result.append(stock)
    except Exception as ex:
        import traceback
        type_, value_, traceback_ = sys.exc_info()
        tb = traceback.format_tb(traceback_)
        print(F"Exception raised stock={stock} {str(ex)} - {str(tb)}")

# Print the search results
print("\nResult stocks:")
for k, stock in enumerate(result):
    print(f"{k+1}. {stock}")
