import pandas as pd
import akshare as ak

stock_df = ak.stock_info_a_code_name()
stock_df.to_csv("csv/AA.csv", index=False)


stock_df = ak.stock_info_sh_name_code()
stock_df.to_csv("csv/SS.csv", index=False)
  

stock_df = ak.stock_info_sz_name_code()
stock_df.to_csv("csv/SZ.csv", index=False)