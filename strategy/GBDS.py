# 顧比倒数抄底
# Import necessary libraries
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import talib
from pandas_datareader import data as pdr
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from strategy.Strategy import Strategy

#Green candle (includes pseudo red)
def green_candle(data, index): # positive index
    return (data['Close'].iloc[-index] > data['Close'].iloc[-index - 1]) 
    
def red_candle(data, index):
    return (data['Close'].iloc[-index] < data['Close'].iloc[-index - 1])

# Find trading Amount
def find_amount(data,i): # positive i
    return data['Volume'].iloc[-i] * data ['Close'].iloc[-i]

# Find lowest low and its index
def find_lowest_low_and_index(data, start, end):
    lowest_low = data['Low'].iloc[-start:-end-1:-1].min()

    for i in range(-start, -end-1, -1):
        if data['Low'].iloc[i] == lowest_low:
            #print(f"lowest_low = {lowest_low} @ {i}")
            return lowest_low, -i  # i is negative. i = lowest_low_index

    return None, None

def find_ascending_red_candles(data, lowest_low_index, end_index): # negative index
    count = 0
    prev_high = None
    for i in range(lowest_low_index, end_index-1, -1):
        if red_candle(data, i):
            #print(f"Day[{i}]: Open = {data['Open'][i]}, Close = {data['Close'][i]}, High = {data['High'][i]}, Low = {data['Low'][i]}")
            if prev_high is None or data['High'].iloc[i] > prev_high:
                #print(f"Red candle {count} @ {i}; Close{i} = {data['Close'][i]}, Close{i-1} = {data['Close'][i-1]}") 
                prev_high = data['High'].iloc[i]
                count += 1
        if count >= 3:
            return prev_high, i #return breakout_price and breakout_index
    return None, None

def check_gubi_breakout(data, breakout_price, lowest_low_index):# negative index
    #Check if the Close of day[-1] is the ONLY candle with price break out 
    #breakout_price happened inside the time window [-1 to lowest_low_index].   

    breakout_count = 0  # Counter for breakout occurrences
    for i in range(-1, -lowest_low_index, -1):
        if data['Close'].iloc[i] > breakout_price:
            breakout_count += 1  # Increment the breakout count
            if breakout_count > 1:
                break
    if breakout_count == 1 and i == -1:
        return True
    else:
        return False

class GBDS(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        # Find lowest "Low" index
        start_index = 2  # Replace with your desired start index
        end_index = 15  # Replace with your desired end index
        df1 = df.rename(columns=str.capitalize)
        # if 'OPEN' in self.df.columns:
        #     df = self.df.rename(columns={'OPEN': 'Open', 'CLOSE':'Close', 'HIGH' : 'High', 'LOW': 'Low'})
        
        lowest_low, lowest_low_index = find_lowest_low_and_index(df1, start_index, end_index) # lowest_low_index is negative
            #print(f"lowest_low_index = {lowest_low_index}; end_index = {end_index}")
        
        if end_index - lowest_low_index  < 3:
            return False #skip because not enough length for GuBi breakout
    
        # GuBi breakout price and its index
        breakout_price, breakout_index = find_ascending_red_candles(df1, -lowest_low_index, -end_index)
        #print(f"breakout_price = {breakout_price}, breakout_index = {breakout_index}")
        
        if breakout_price is not None and check_gubi_breakout(df1, breakout_price, lowest_low_index):
            return True

        return False

if __name__ == "__main__":
    # Get the CSV file name from the user
    root = Tk()
    root.withdraw()
    csvfilename = askopenfilename(title="Select CSV File")
    root.destroy()

    # Load the stock symbols from the CSV file
    stocklist = pd.read_csv(csvfilename, engine="python", encoding="ISO-8859-1")

    # Set up yfinance
    yf.pdr_override()
    start = dt.datetime.now() - dt.timedelta(days=100)
    now = dt.datetime.now()

    # Initialize list of stocks that meet the criteria
    exportList = []

    # Iterate through each stock in the list
    for i in range(len(stocklist)):
        stock = stocklist.iloc[i]["Symbol"]
        print(f"{i+1}/{len(stocklist)} {stock}")
        
        # Retrieve stock data from Yahoo Finance
        df = None
        try:
            df = yf.download(stock, start, now)
        except (KeyError, IndexError) as e:
            print(f"Error: {str(e)}")
            print(f"The problematic data frame is:\n{df}")        
            continue
        
        # Check for availability of Low column
        if len(df) < 25:
            print(df)
            continue
        '''
        # Check trading amount
        if find_amount(df,1) < 5e7:
            print(f"Turnover too low!")
            continue
        
        # Print the first 16 days records
        print(df.head(6).to_string())
        '''
        # Find lowest "Low" index
        start_index = 2  # Replace with your desired start index
        end_index = 15  # Replace with your desired end index
        lowest_low, lowest_low_index = find_lowest_low_and_index(df, start_index, end_index) # lowest_low_index is negative
        #print(f"lowest_low_index = {lowest_low_index}; end_index = {end_index}")
        
        if end_index - lowest_low_index  < 3:
            continue #skip because not enough length for GuBi breakout
    
        # GuBi breakout price and its index
        breakout_price, breakout_index = find_ascending_red_candles(df, -lowest_low_index, -end_index)
        #print(f"breakout_price = {breakout_price}, breakout_index = {breakout_index}")
        
        if breakout_price is not None and check_gubi_breakout(df, breakout_price, lowest_low_index):
            gubi_breakout = True
            #print(f"GUBI Breakout for {stock} @ -1")
            exportList.append(stock)

    # Print the search results
    print("\nStocks that possibly meet GUBI breakout (顧比倒数抄底):")
    for k, stock in enumerate(exportList):
        print(f"{k+1}. {stock}")
