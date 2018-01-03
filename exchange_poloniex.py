import ccxt
from datetime import datetime, timedelta, timezone
import pandas as pd

ex = ccxt.poloniex()
mkts = ex.load_markets()


def btc_to_satoshi(btc):
    return btc*100000000

def fetch_df(days_back = 1, timestep = '15m', pair_name = 'MAID/BTC'):
    ohlcv = ex.fetch_ohlcv(pair_name,
                           timestep,
                           since = int((datetime.utcnow() - timedelta(days = days_back)).replace(tzinfo=timezone.utc).timestamp())*1000
                          )
    df = pd.DataFrame(
        {
#         "posix":x[0]/1000,
         "datetime":datetime.fromtimestamp(x[0]/1000).replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
         "open":btc_to_satoshi(x[1]),
         "high":btc_to_satoshi(x[2]),
         "low":btc_to_satoshi(x[3]),
         "close":btc_to_satoshi(x[4]),
         "volume":x[5]
        }
        for x in ohlcv)
    return df

def save_df(days_back = 1, appended_name = ''):
    df = fetch_df(days_back)
    df.to_csv(path_or_buf='./dataframes/poloniex_'+appended_name)

def load_df(appended_name = ''):
    path = './dataframes/poloniex_'+appended_name
    col_names = ['close', 'datetime', 'high', 'low', 'open', 'volume']
    df = pd.read_csv(path, header=0, names=col_names) 
    df = pd.DataFrame(df)
    df.index.name = 'datetime'
    df.drop(labels = ['datetime'], axis = 1, inplace = True)
#    df = df[['open', 'high', 'close']]
    return df