import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import datetime as dt
import string
import config

def get_pubsub_message(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    return pubsub_message

def get_list_of_stock_symbol():
    
    prefix = ['NUMBER'] + list(string.ascii_uppercase)
    all_symbol = []
    for p in tqdm(prefix):
        url="https://classic.set.or.th/set/commonslookup.do?"
        res = requests.get(url=url,
                          params={
                              "language" :"en",
                              "country":"th",
                              "prefix": p
                          })
        soup = BeautifulSoup(res.content, 'html.parser')    
        symbol = soup.findAll("table")[0]    
        symbol_df = pd.read_html(str(symbol))[0]
        all_symbol.append(symbol_df)
        time.sleep(0.5)
    return all_symbol


