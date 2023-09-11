#https://discord.com/channels/898763842992095262/899105966358954074/963972681458409542
#均线金三角
import pandas as pd
import datetime as dt
import yfinance as yf
from pandas_datareader import data as pdr
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import dateutil.relativedelta as rd
from datapackage import Package
import sys

yf.pdr_override()
#start = dt.datetime(2021,4,12)
now = dt.datetime.now()
start = now + rd.relativedelta(months=-2)

print(F"Start date: {start}")

# filepath="NYSE_screener.csv"
# stocklist = pd.read_csv(filepath)

#https://datahub.io/core/s-and-p-500-companies#python
package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        stocklist=(resource.read())

stocklist_nq=None
if len(sys.argv) == 2 and sys.argv[1] == "nq":
    package = Package('https://datahub.io/core/nasdaq-listings/datapackage.json')
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            stocklist_nq=(resource.read())
    
if stocklist_nq is not None:
    stocklist=stocklist+stocklist_nq

#exportList = pd.DataFrame(columns=["Stock"])
exportList = []
# for i in stocklist.index:
#     stock=str(stocklist["Symbol"][i])

for i in stocklist:
    stock=i[0]
    try:
        df = pdr.get_data_yahoo(stock,start,now)
        smaUsed=[5,10,20]
        for x in smaUsed:
            sma=x
            df["SMA_"+str(sma)]=round(df.iloc[:,4].rolling(window=sma).mean(),3)
        moving_average_5=df["SMA_5"][-1]
        moving_average_10=df["SMA_10"][-1]
        moving_average_20=df["SMA_20"][-1]
        try:
            moving_average_10_1past=df["SMA_10"][-2]
            moving_average_20_1past=df["SMA_20"][-2]
        except Exception:
            moving_average_10_1past=0
            moving_average_20_1past=0

        if(moving_average_5>moving_average_10):
            cond1=True
        else:
            cond1=False

        if(moving_average_10>moving_average_20):
            cond2=True
        else:
            cond2=False

        if(moving_average_10_1past<moving_average_20_1past):
            cond3=True
        else:
            cond3=False
        if(cond1 and cond2 and cond3):
            #exportList = exportList.append({"Stock":stock},ignore_index=True)
            expportList = exportList.append(stock)
    except Exception as ex:
        import traceback
        type_, value_, traceback_ = sys.exc_info()
        tb = traceback.format_tb(traceback_)
        print(F"Exception raised {str(ex)} - {str(tb)}")
        print("No data on " + stock)
        
print(exportList)