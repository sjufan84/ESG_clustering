import alpaca_trade_api as tradeapi
import datetime as dt
from dotenv import load_dotenv
import sys
import os
import pandas as pd


#import environment variables
load_dotenv()
APCA_API_KEY_ID = os.getenv('APCA-API-KEY-ID')
APCA_API_SECRET_KEY = os.getenv('APCA-API-SECRET-KEY')


alpaca = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

        

# Alpaca functions (recently updated from get_barset (deprecated) to get_bars


# Get bars:
def get_historical_dataframe(symbol, start, end, timeframe):
    ticker_df = alpaca.get_bars(symbol=symbol, timeframe=timeframe, start=start, end = end, limit = 5000).df
    return ticker_df


# Get historical Crypto data:
def get_crypto_bars(symbol, start, end, timeframe, limit):
    crypto_df = alpaca.get_crypto_bars(symbol=symbol, timeframe=timeframe, start=start, end=end, limit=limit, exchanges='CBSE').df
    return crypto_df

def get_news(symbol, start, end, limit):
    news_df = alpaca.get_news(symbol=symbol, start=start, end=end, limit=limit)
    return news_df


