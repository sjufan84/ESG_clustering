# %%
import datetime as dt
from dotenv import load_dotenv
import sys
import os
import pandas as pd
import requests
import json
from pathlib import Path


# %%
#import environment variables
load_dotenv()
ESG_api_key = os.getenv('ESG_API_KEY')
rapidapi_host = 'esg-environmental-social-governance-data.p.rapidapi.com'

# %%


url = "https://esg-environmental-social-governance-data.p.rapidapi.com/search"
headers = {
    'x-rapidapi-host': "esg-environmental-social-governance-data.p.rapidapi.com",
    'x-rapidapi-key': "ed5753e239msh35bbc80821a70dcp1cc1c1jsn993b485f9da5"
    }


tickers = ['CRM', 'NVDA', 'MSFT', 'BBY', 'LIN', 'ADBE', 'INTU', 'POOL', 'LRCX', 'TSLA']

def get_esg_score(ticker):
    querystring = {'q' : ticker}
    ticker = ticker
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return response

ESG_df = pd.DataFrame()
for ticker in tickers:
    querystring = {'q' : ticker}
    ticker = ticker
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    ticker_ESG_df = pd.DataFrame.from_dict(response)
    ESG_df = pd.concat([ticker_ESG_df, ESG_df])
    print(ticker_ESG_df, ESG_df)

ESG_df.to_csv(Path('ESGScores.csv'))
    



# %%



