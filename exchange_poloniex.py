import ccxt
from datetime import datetime, timedelta, timezone
import pandas as pd

ex = ccxt.poloniex()
mkts = ex.load_markets()


def btc_to_satoshi(btc):
    return btc*100000000

def fetch_df(days_back = 1):
    ohlcv = ex.fetch_ohlcv("EMC2/BTC", '5m', since = int((datetime.utcnow() - timedelta(days = days_back)).replace(tzinfo=timezone.utc).timestamp())*1000)
    df = pd.DataFrame({"posix":x[0]/1000, "datetime":datetime.fromtimestamp(x[0]/1000).replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'), "open":btc_to_satoshi(x[1]), "high":btc_to_satoshi(x[2]), "low":btc_to_satoshi(x[3]), "close":btc_to_satoshi(x[4]), "volume":x[5]} for x in ohlcv)
    return df

def save_df(days_back = 1):
    df = fetch_df(days_back)
    df.to_csv(path_or_buf='./dataframes/poloniex_emc')

def load_df():
    df = pd.read_csv('./dataframes/poloniex_emc')
    return df