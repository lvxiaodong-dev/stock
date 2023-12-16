import yfinance as yf

# N周期前的M周期内的第T个最小值到当前周期的周期数.
# 用法:FINDLOWBARS(VAR,N,M,T):VAR在N日前的M天内第T个最低价到当前周期的周期数.

#https://raw.githubusercontent.com/jones2000/HQChart/c0d7f75a85e91380d6e396e72ba9bff15776fadc/wechathqchart/umychart.complier.wechat.js
def FINDLOWBARS(data, n, m, t):
    count = len(data)
    result = [10000] * count
    values = [None] * count
    for i in range(count - 1, -1, -1):
        aryValue = []
        for j in range(n, m):
            index = i - j
            if index < 0:
                break
            item = data[index]
            aryValue.append({"Value": item, "Period": j})
        if len(aryValue) > 0:
            aryValue.sort(key=lambda x: x["Value"])
            index = t - 1 if t > 0 else 0
            index = min(index, len(aryValue) - 1)
            result[i] = aryValue[index]["Period"]
            values[i] = aryValue[index]["Value"]
    return result, values

    #N周期前的M周期内的第T个最小值.
    #用法:FINDLOW(VAR,N,M,T):VAR在N日前的M天内第T个最低价
def FINDLOW(data,n,m,t):
    count = len(data)
    result = [10000] * count
    
    for i in range(count - 1, -1, -1):
        aryValue=[]
        for j in range(n,m):
            index=i-j
            if index<0:
                break
            item=data[index]
            aryValue.append(item)

        if len(aryValue) > 0:
            aryValue.sort()
            index=t-1
            if index<0:
                index=0
            elif index>=len(aryValue):
                index=len(aryValue)-1
            result[i]=aryValue[index]

    return result

#N周期前的M周期内的第T个最大值.
#用法:FINDHIGH(VAR,N,M,T):VAR在N日前的M天内第T个最高价
def FINDHIGH(data, n, m, t):
    count = len(data)
    result = [0] * count

    for i in range(count - 1, -1, -1):
        ary_value = []
        for j in range(n, m):
            index = i - j
            if index < 0:
                break
            item = data[index]
            ary_value.append(item)

        if len(ary_value) > 0:
            ary_value.sort(reverse=True)
            index = t - 1
            if index < 0:
                index = 0
            elif index >= len(ary_value):
                index = len(ary_value) - 1
            result[i] = ary_value[index]

    return result

# https://raw.githubusercontent.com/jones2000/HQChart/c0d7f75a85e91380d6e396e72ba9bff15776fadc/wechathqchart/umychart.complier.wechat.js
# LAST(X,A,B):持续存在.
# 用法:
# LAST(CLOSE>OPEN,10,5) 
# 表示从前10日到前5日内一直阳线
# 若A为0,表示从第一天开始,B为0,表示到最后日止
def LAST(data, n, n2):
    result = [False] * len(data)
    if n2 <= 0:
        n2 = len(data) - 1
    if n2 > n:
        return result

    day = 0
    for i in range(len(data)):
        day = 0
        start = i - n
        end = i - n2
        if start < 0 or end < 0:
            continue

        for j in range(start, len(data)):
            if j > end:
                break
            day += 1
            if not data[j]:
                break

        if day == end - start + 1:
            result[i] = True

    return result

class MyTA:
    # Find trading Amount
    @staticmethod
    def find_amount(data,i): # positive i
        return data['Volume'].iloc[-i] * data ['Close'].iloc[-i]

    @staticmethod
    def find_low_9(data):
        low_9_indices = []
        
        for i in range(8, len(data)):
            # Check if current day is a potential Low 9
            if data["Close"].iloc[i] < data["Close"].iloc[i - 4]:
                # Check if all conditions for a Low 9 are met
                if (data["Close"].iloc[i - 8] > data["Close"].iloc[i - 4] and
                    data["Close"].iloc[i - 7] > data["Close"].iloc[i - 4] and
                    data["Close"].iloc[i - 6] > data["Close"].iloc[i - 4] and
                    data["Close"].iloc[i - 5] > data["Close"].iloc[i - 4] and
                    data["Low"].iloc[i - 8] > data["Low"].iloc[i - 7] and
                    data["Low"].iloc[i - 7] > data["Low"].iloc[i - 6] and
                    data["Low"].iloc[i - 6] > data["Low"].iloc[i - 5] and
                    data["Low"].iloc[i - 5] > data["Low"].iloc[i - 4]):
                    low_9_indices.append(i - 4)
        
        return low_9_indices

    # Check for a complete downward TD series
    @staticmethod
    def confirm_low9(data, i): # call with positive i
        for k in range(0, 9):
            if data['Close'].iloc[-k-i] >= data['Close'].iloc[-k-i-4]:
                return False
            if k == 8 and data['Close'].iloc[-k-i-1] < data['Close'].iloc[-k-i-5]:
                #print(f"No low 9, k = {k}")
                return False
        return True

    @staticmethod
    def price_flip(data, index):
        if index - 4 >= 0 and index - 1 >= 0:
            return data['Close'].iloc[index] > data['Close'].iloc[index - 4] and \
                data['Close'].iloc[index - 1] < data['Close'].iloc[index - 4]
        return False

    # Determin Low of days[-2],[-3] < Low of days[-4], [-5]
    @staticmethod
    def perfect_low_9(data, start): # call with positicve start
        if min(data['Low'].iloc[-start], data['Low'].iloc[-start-1]) < min(data['Low'].iloc[-start-2], data['Low'].iloc[-start-3]):
            #print(f"perfect low_9 @ {i}")
            return True

    @staticmethod
    def find_5_day_bottom_index(data, start, end):
        if start < 2:
            return None  # Skip the rest of execution

        lowest_low = data['Low'].iloc[-start:-end-1:-1].min()

        for i in range(-start, -end-1, -1):
            if data['Low'].iloc[i] == lowest_low:
                if (-start + i <= -2) and (data['Low'].iloc[i-2] > data['Low'].iloc[i-1] > data['Low'].iloc[i]) and \
                    (data['Low'].iloc[i+1] > data['Low'].iloc[i+2] > data['Low'].iloc[i]):
                    return -i  # Return positive index

        return None  # Return None if no 5-day bottom index is found

    @staticmethod
    def find_ascending_high(data, start, end): # positive index
        count = 0
        prev_high = data['High'].iloc[-start]
        for i in range(-start, -end-1, -1):

            if prev_high is None or data['High'].iloc[i] > prev_high:
                prev_high = data['High'].iloc[i]
                count += 1
                
            if count >= 3:
                #print(f"count={count}; prev_high={prev_high}")
                return prev_high, -i #return breakup_price and breakup_price_index (positive index)
            
        return None, None

    # low 9 location
    @staticmethod
    def find_low_9_location(data, start, end):  # Positive start and end
        for i in range(-start, -end - 1, -1):
            low_9_found = MyTA.confirm_low9(data, -i)
            #print(f"Checking index {i}: Low 9 found: {low_9_found}")
            if low_9_found:
                #print(f"{stock}: low 9 @ {i}")
                return -i  # Return a positive number
                break # stop the search
        return None

    @staticmethod        
    def find_perfect_low_9(df, i): # call with negative i
        for k in range(0, 9):  # Start from k = 0
            if df['Close'].iloc[i - k] >= df['Close'].iloc[i - k - 4]:
                return False
            if k == 8 and df['Close'].iloc[i - k - 1] < df['Close'].iloc[i - k - 5]:
                return False
        perfect_low_9 = min(df['Low'].iloc[i - 1], df['Low'].iloc[i - 2]) < min(df['Low'].iloc[i - 3], df['Low'].iloc[i - 4])
        
        return perfect_low_9

    # Cross up
    @staticmethod
    def cross_up(parameter1, parameter2, i): # positive i
        return (parameter1.iloc[-i-1] < parameter2.iloc[-i] < parameter1.iloc[-i])

    # Pseudo Green candle
    @staticmethod
    def pseudo_green_candle(data,i): # positive i
        if data['Close'].iloc[-i] < data['Close'].iloc[-i-1] and data['Close'].iloc[-i] > data['Open'].iloc[-i] :
            return True        
    #成交额
    @staticmethod
    def small_volume(df):
        last_volume = df['Volume'].iloc[-1]
        last_close = df['Close'].iloc[-1]
        last_dollar_volume = last_volume * last_close
        if last_dollar_volume < 10000:
            return True
        return False

    @staticmethod
    def small_market_value(code):
        try:
            market_cap = yf.Ticker(code).fast_info.market_cap
            #print(stock, market_cap)
            #100 亿
            if market_cap < 10000000000:
                #print(F"Skip {code} since its cap {market_cap} is small")
                return True
        except Exception as e:
            #print("ERROR: failed to get market_cap")
            pass
        return False
    
    @staticmethod
    def body_low(df, i):
        return df["Close"].iloc[-i] if df["Close"].iloc[-i] <= df["Open"].iloc[-i] else df["Open"].iloc[-i]
    
    @staticmethod
    def body_high(df, i):
        return df["Close"].iloc[-i] if df["Close"].iloc[-i] >= df["Open"].iloc[-i] else df["Open"].iloc[-i]

    # Define Function to find Top Shape pattern at day[-i]
    @staticmethod
    def top_shape(data, i): #i >= 2
        if i < 2:
            return False
        if (data['High'].iloc[-i-1] < data['High'].iloc[-i]) and (data['High'].iloc[-i] > data['High'].iloc[-i+1]) and \
        (data['Low'].iloc[-i-1]  < data['Low'].iloc[-i]) and  (data['Low'].iloc[-i]  > data['Low'].iloc[-i+1]):
            #print(f"Top Shape occurred at {-i}: left={data['High'].iloc[-i-1]}, mid={data['High'].iloc[-i]}, right={data['High'].iloc[-i+1]})")
            return True
        else:
            return False

    # Define Function to find Bottom Shape pattern at day [-i]
    @staticmethod
    def bottom_shape(data, i): # i >= 2
        if i < 2:
            return False    
        if (data['High'].iloc[-i-1] > data['High'].iloc[-i]) and (data['High'].iloc[-i] < data['High'].iloc[-i+1]) and \
        (data['Low'].iloc[-i-1]  > data['Low'].iloc[-i]) and  (data['Low'].iloc[-i]  < data['Low'].iloc[-i+1]):
            #print(f"Bottom Shape occurred at {-i}: left={data['Low'].iloc[-i-1]}, mid={data['Low'].iloc[-i]}, right={data['Low'].iloc[-i+1]})")
            return True
        else:
            return False

    # green candle
    @staticmethod
    def green_candle(data, i): #positive i, geen candle at [-i]
        if len(data) < 2:
            return False
        
        if data['Close'].iloc[-i] > data['Close'].iloc[-i-1]:
            #print(f"green candle: {data['Close'][-i] - data['Open'][-i]}")
            return True
        else:
            return False
        
    #red candle (includes pseudo green)
    @staticmethod
    def red_candle(data, i): #positive i, red candle at [-i]
        if len(data) < 2:
            return False
        
        if (data['Close'].iloc[-i] < data['Close'].iloc[-i-1]):
            #print(f"red candle: {data['Close'][-i] - data['Open'][-i]}")        
            return True
        else:
            return False
        
    # SMA Calculate
    @staticmethod
    def calculate_ma_slope(data, ma_window, bar_number):
        ma = data['Close'].rolling(ma_window).mean()
        ma_slope = (ma.iloc[-1] - ma.iloc[-bar_number]) / (bar_number - 1)
        return ma, ma_slope
    
    @staticmethod
    def calculate_ema_slope(data, ma_window, bar_number):
        ema = data.ewm(span=ma_window, adjust=False).mean()
        ema_slope = (ema.iloc[-1] - ema.iloc[-bar_number]) / (bar_number - 1)
        return ema, ema_slope