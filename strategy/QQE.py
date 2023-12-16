import numpy as np
import ta
from libs.MyTA import MyTA as mta
from strategy.Strategy import Strategy

class QQE(Strategy):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, df, info):
        df1 = self.YahooDf(df)
        # QQE indicator
        # Calculate LC (REF(CLOSE, 1))
        df1['LC'] = df1['Close'].shift(1)

        # Calculate TEMP1 (MAX(CLOSE-LC, 0))
        df1['TEMP1'] = np.maximum(df1['Close'] - df1['LC'], 0)

        # Calculate TEMP2 (ABS(CLOSE-LC))
        df1['TEMP2'] = np.abs(df1['Close'] - df1['LC'])

        # Calculate RSI using ta-lib's RSI indicator
        rsi_period = 6
        df1['RSI'] = ta.momentum.RSIIndicator(df1['Close'], rsi_period).rsi()

        # Calculate RSI_PERIOD
        RSI_PERIOD = 6

        # Calculate COND (IF(RSI>=50, 1, -1))
        df1['COND'] = np.where(df1['RSI'] >= 50, 1, -1)

        # Calculate QQELONG (SUM(COND, TOTALBARSCOUNT))
        df1['QQELONG'] = df1['COND'].cumsum()

        # Calculate WILDERS_PERIOD
        WILDERS_PERIOD = RSI_PERIOD * 2 - 1

        # Calculate RSIMA (EMA(RSI, 5))
        df1['RSIMA'] = ta.trend.EMAIndicator(df1['RSI'], window=5).ema_indicator()

        # Calculate ATRRSIMA (ABS(RSIMA - REF(RSIMA, 1)))
        df1['ATRRSIMA'] = np.abs(df1['RSIMA'] - df1['RSIMA'].shift(1))

        # Calculate DAR (EMA(ATRRSIMA, WILDERS_PERIOD) * 1.61)
        df1['DAR'] = ta.trend.EMAIndicator(df1['ATRRSIMA'], window=WILDERS_PERIOD).ema_indicator() * 1.61

        # Calculate DAR1 (EMA(ATRRSIMA, WILDERS_PERIOD) * 3)
        df1['DAR1'] = ta.trend.EMAIndicator(df1['ATRRSIMA'], window=WILDERS_PERIOD).ema_indicator() * 3

        # Calculate NEWSHORTBAND (RSIMA + DAR)
        df1['NEWSHORTBAND'] = df1['RSIMA'] + df1['DAR']

        # Calculate NEWLONGBAND (RSIMA - DAR)
        df1['NEWLONGBAND'] = df1['RSIMA'] - df1['DAR']

        # Calculate NEWSHORTBAND1 (RSIMA + DAR1)
        df1['NEWSHORTBAND1'] = df1['RSIMA'] + df1['DAR1']

        # Calculate NEWLONGBAND1 (RSIMA - DAR1)
        df1['NEWLONGBAND1'] = df1['RSIMA'] - df1['DAR1']

        # Calculate LONGBAND
        df1['LONGBAND'] = np.where((df1['RSIMA'].shift(1) > df1['RSIMA'].shift(2)) & (df1['RSIMA'] > df1['RSIMA'].shift(2)),
                                    np.maximum(df1['RSIMA'].shift(2), df1['NEWLONGBAND']),
                                    df1['NEWLONGBAND'])

        # Calculate SHORTBAND
        df1['SHORTBAND'] = np.where((df1['RSIMA'].shift(1) < df1['RSIMA'].shift(2)) & (df1['RSIMA'] < df1['RSIMA'].shift(2)),
                                    np.minimum(df1['RSIMA'].shift(2), df1['NEWSHORTBAND']),
                                    df1['NEWSHORTBAND'])

        # Calculate LONGBAND1
        df1['LONGBAND1'] = np.where((df1['RSIMA'].shift(1) > df1['RSIMA'].shift(2)) & (df1['RSIMA'] > df1['RSIMA'].shift(2)),
                                    np.maximum(df1['RSIMA'].shift(2), df1['NEWLONGBAND1']),
                                    df1['NEWLONGBAND1'])

        # Calculate SHORTBAND1
        df1['SHORTBAND1'] = np.where((df1['RSIMA'].shift(1) < df1['RSIMA'].shift(2)) & (df1['RSIMA'] < df1['RSIMA'].shift(2)),
                                      np.minimum(df1['RSIMA'].shift(2), df1['NEWSHORTBAND1']),
                                      df1['NEWSHORTBAND1'])

        # Calculate TREND2
        df1['TREND2'] = np.where((df1['RSIMA'] > df1['SHORTBAND1'].shift(1)) & (df1['RSIMA'].shift(1) <= df1['SHORTBAND1']),
                                  1, 0)

        # Calculate FASTLY1
        df1['FASTLY1'] = np.where(df1['TREND2'] == 1, df1['LONGBAND1'], df1['SHORTBAND1'])

        # Calculate BASIS1 (MA(FASTLY1-50, 50))
        df1['BASIS1'] = ta.volatility.bollinger_mavg(df1['FASTLY1'] - 50, window=50)

        # Calculate DEV1 (0.35 * STD(FASTLY1-50, 50))
        df1['DEV1'] = 0.35 * ta.volatility.bollinger_mavg(df1['FASTLY1'] - 50, window=50, fillna=True)

        # Calculate UPPER1 (BASIS1 + DEV1)
        df1['UPPER1'] = df1['BASIS1'] + df1['DEV1']

        # Calculate LOWER1 (BASIS1 - DEV1)
        df1['LOWER1'] = df1['BASIS1'] - df1['DEV1']

        # Calculate TREND1
        df1['TREND1'] = np.where((np.logical_or(df1['RSIMA'] > df1['SHORTBAND'].shift(1), df1['SHORTBAND'].shift(1) > df1['RSIMA'])) |
                                  (np.logical_or(df1['RSIMA'] > df1['LONGBAND'].shift(1), df1['LONGBAND'].shift(1) > df1['RSIMA'])),
                                  1,
                                  np.where(np.logical_or(df1['RSIMA'] > df1['SHORTBAND'].shift(1), df1['SHORTBAND'].shift(1) > df1['RSIMA']),
                                          -1,
                                          0))

        # Calculate CROSS1
        df1['CROSS1'] = np.where(np.logical_or(df1['RSIMA'] > df1['LONGBAND'].shift(1), df1['LONGBAND'].shift(1) > df1['RSIMA']),
                                  -1,
                                  0)

        # Calculate FASTLY
        df1['FASTLY'] = np.where(df1['TREND1'] == 0, df1['RSIMA'],
                                  np.where(df1['TREND1'] == -1, df1['LONGBAND'], df1['SHORTBAND']))

        # Calculate QQE1 (FASTLY - 50)
        df1['QQE1'] = df1['FASTLY'] - 50

        # Calculate RSIMA1 (RSIMA - 50)
        df1['RSIMA1'] = df1['RSIMA'] - 50

        # Calculate BASIS (MA(FASTLY - 50, 50))
        df1['BASIS'] = ta.volatility.bollinger_mavg(df1['FASTLY'] - 50, window=50)

        # Calculate DEV (0.35 * STD(FASTLY - 50, 50))
        df1['DEV'] = 0.35 * ta.volatility.bollinger_mavg(df1['FASTLY'] - 50, window=50, fillna=True)

        # Calculate UPPER (BASIS + DEV)
        df1['UPPER'] = df1['BASIS'] + df1['DEV']

        # Calculate LOWER (BASIS - DEV)
        df1['LOWER'] = df1['BASIS'] - df1['DEV']

        # Calculate EMA(CLOSE, 20)
        df1['EMA20'] = ta.trend.EMAIndicator(df1['Close'], window=20).ema_indicator()

        # Calculate EMA(CLOSE, 60)
        df1['EMA60'] = ta.trend.EMAIndicator(df1['Close'], window=60).ema_indicator()

        # Calculate EMA(CLOSE, 120)
        df1['EMA120'] = ta.trend.EMAIndicator(df1['Close'], window=120).ema_indicator()

        # Calculate COMPARISON
        df1['COMPARISON'] = (df1['EMA20'] - df1['EMA60']) / df1['EMA120'] * 500

        df1['LINE1'] = 0

        # # buy_condition
        # if df['COMPARISON'].iloc[-1] < 0 and df['QQE1'].iloc[-1] > 0 and df['QQE1'].iloc[-2] <= 0:
        #   qqe_condition = 1
        # else:
        #   qqe_condition = 0

        def cross_above(series1, value):
            return (series1.shift(1) < value) & (series1 > value)

        # Calculate the buy_condition
        if df1['COMPARISON'].iloc[-1] < 0 and cross_above(df1['QQE1'], 0).iloc[-1]:
            qqe_condition = 1
        else:
            qqe_condition = 0

        if qqe_condition:
            return True
        return False