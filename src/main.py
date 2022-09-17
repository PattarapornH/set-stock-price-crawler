import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import datetime as dt
import string
import config
import utils
import base64
import time
import logging

logger = logging.getLogger(__name__)

def get_pubsub_message(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    return pubsub_message

def get_list_of_stock_symbol():
    
    logger.info("Getting all symbol")
    prefix = ['NUMBER'] + list(string.ascii_uppercase)
    all_symbol = []
    for p in prefix:
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
    all_symbol = pd.concat(all_symbol)
    return all_symbol



def get_stock_price(all_symbol, prev_day):
    yf_ticker = [f"{s}.BK" for s in all_symbol['Symbol'].values]
    yf_ticker = ' '.join(yf_ticker)
    history = yf.download(tickers=yf_ticker,start=prev_day)
    history = history.stack(level=1).reset_index().copy()
    history['level_1'] = history['level_1'].apply(lambda s: s.split(".")[0])
    history.rename(columns={"level_1":"Symbol","Date":"RecordDate","Adj Close":"AdjClose","Company/Security Name":"Name"},inplace=True)
    return history

    
def main(event, context):
    
    messages = get_pubsub_message(event, context)
    if messages == "monthly update stock":
        pass
    else:
        raise Exception(f"{messages} messages does not support")
        
    current = dt.datetime.now()
    prev_7d = current - dt.timedelta(days=7)
    all_symbol = get_list_of_stock_symbol()
    price = get_stock_price(all_symbol=all_symbol, prev_day=prev_7d)
    utils.write_dataframe_to_bq(dataframe=price,table_name=config.BQ_PRICE_TABLE_NAME)

    delete_outdated_query = f"""
    DELETE `{config.GCP_PROJECT}.{config.BQ_DATASET}.{config.BQ_PRICE_TABLE_NAME}`
    WHERE RecordDate < DATE_SUB(CURRENT_DATE("Asia/Bangkok"),INTERVAL 1 YEAR)
    """

    utils.query_table(query=delete_outdated_query)
