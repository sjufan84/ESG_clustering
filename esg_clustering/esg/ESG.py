# %%
import datetime as dt
from dotenv import load_dotenv
import sys
import os
import pandas as pd
import requests
import json
from pprint import pprint

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


def get_esg_env_score(ticker):
    querystring = {'q' : ticker}
    ticker = ticker
    
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    try: 
        [env_score, gov_score] = response[0]['environment_score']['governance_score']
    except:
        pass
    return env_score, gov_score

test = get_esg_env_score('TSLA')
print(test)












# %%


# %%



