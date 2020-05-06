import pandas as pd
import pandas_datareader.data as web
import pandas_datareader as pdr
from datetime import datetime
from autotrd81app import models 
import time

baseCurr = "USD"
ALPHAVANTAGE_API_KEY = 'RQ1VVYRHKG906UUJ'
#Get currency rates for below symbols
# USDAUD=X, BTCUSD=X, USDINR=X,
def getCurrLTPs(strategy):
    lstCurr = None
    dictCurr = {"SS_CURR_FUT_PAIRS": {"name": ['EURINR', 'GBPINR', 'JPYINR', 'USDINR'], 
                    "yahoo":['EURINR=X', 'GBPINR=X', 'JPYINR=X', 'USDINR=X'], "av-forex":['EUR/INR', 'GBP/INR', 'JPY/INR', 'USD/INR']}, 
                "SS_REV_CURR_PAIRS": {"name": ["AED", "AUD","CAD","CHF","DKK","EUR","GBP","INR","JPY","NOK","NZD","USD"], 
                    "yahoo":['AUDUSD=X', 'CADUSD=X', 'CHFUSD=X', 'DKKUSD=X','EURUSD=X', 'GBPUSD=X','JPYUSD=X', 'NZDUSD=X'], 
                    "av-forex":['AUD/USD', 'CAD/USD', 'CHF/USD', 'DKK/USD','EUR/USD', 'GBP/USD','JPY/USD', 'NZD/USD']}, 
                "SS_REV_CURR_BTC": {"name": ['BTCUSD'], "yahoo":['BTCUSD=X'], "av-forex":['BTC/USD']}
            }
    source = "yahoo"    #"av-forex"
    if source=="yahoo":
        lstCurr = dictCurr.get(strategy, {}).get(source)
        print(f"yahoo lstCurr:{lstCurr}")
        pdAllCurr = web.get_quote_yahoo(lstCurr)
        print(f'pdAllCurr:{pdAllCurr}')
    elif source == "av-forex":
        lstCurr = dictCurr.get(strategy, {}).get(source)
        lstCurr = ['AUD/USD', 'CAD/USD', 'CHF/USD', 'DKK/USD']
        #lstCurr = ['AUD/USD', 'CAD/USD', 'CHF/USD', 'DKK/USD','EUR/USD', 'GBP/USD','JPY/USD', 'NZD/USD']
        print(f"av-forex lstCurr:{lstCurr}")
        #f = web.DataReader(["USD/JPY", "BTC/CNY"], "av-forex", api_key=ALPHAVANTAGE_API_KEY)
        maxKeys = 4
        if len(lstCurr) <= maxKeys:    
            pdAllCurr = web.DataReader(lstCurr, "av-forex", api_key=ALPHAVANTAGE_API_KEY)
            print(f'pdAllCurr:{pdAllCurr}')
            time.sleep(5)
            pdAllCurr = web.DataReader(lstCurr, "av-forex", api_key=ALPHAVANTAGE_API_KEY)
            print(f'pdAllCurr:{pdAllCurr}')
        elif len(lstCurr) >maxKeys :
            print(lstCurr[0:maxKeys])
            pd1 = web.DataReader(lstCurr[0:maxKeys], "av-forex", api_key=ALPHAVANTAGE_API_KEY)
            #pd2 = web.DataReader(lstCurr[maxKeys:len(lstCurr)], "av-forex", api_key=ALPHAVANTAGE_API_KEY)
            print(pd1)
            #print(pd2)
        #print(f)
    dictRatesOp = dict(zip(pdAllCurr.index, pdAllCurr['price']))
    #print(dictRatesOp)
    return (dictRatesOp)

#Insert these values in db REFRATES-
def insertCurrLTPs(strategy, inContraId):
    dictRates = getCurrLTPs(strategy)
    dtNow = datetime.utcnow()
    for key,value in dictRates.items():
        key = key.replace('=X','')
        key = key.replace('-','')
        key = key.replace('/','')
        if (len(key)==3) and (key != baseCurr):   key= key + baseCurr
        if value < 0.01:    value *= 100
        print(f'Before inserting data key:{key} dtNow:{dtNow} value:{value} inContraId:{inContraId}')
        recRefRates = models.REFRATES(tradingsymbol=key, timestamp=dtNow, price=value, trade_contra_id=inContraId)
        recRefRates.save()

def getSingleQuoteYahoo(symbol):
    print(f'Entering getSingleQuoteYahoo():: symbol:{symbol}')
    symMappings = {'NIFTY 50':'^NSEI', 'USDINR':'USDINR=X','BTCUSD':'BTCUSD=X'}
    yahooSym = symMappings.get(symbol)
    print(f'symbol:{symbol} yahooSym:{yahooSym}')
    panel_data = web.get_quote_yahoo(yahooSym)        #web.get_quote_yahoo(symbol)
    return (panel_data.iloc[0]['price'])

if __name__ == "__main__":
    #insertCurrLTPs('SS_CURR_FUT_PAIRS', 99999)
    getCurrLTPs("SS_REV_CURR_PAIRS")
    #getCurrLTPs("SS_REV_CURR_PAIRS")