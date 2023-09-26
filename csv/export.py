import pandas as pd
import akshare as ak

# stock_df = ak.stock_info_a_code_name()
# stock_df.to_csv("csv/A1.csv", index=False)


# stock_df = ak.stock_us_spot_em()
# stock_df.to_csv("csv/us_db.csv", index=False)


# stock_df = ak.stock_us_spot()
# stock_df.to_csv("csv/us.csv", index=False)

stock_df = ak.get_us_stock_name()
stock_df.to_csv("csv/us.csv", index=False)
