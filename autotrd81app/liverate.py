import datetime as dt 
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import pandas_datareader as pdr

ALPHAVANTAGE_API_KEY = 'RQ1VVYRHKG906UUJ'
TIINGO_API_KEY = '1447a8381cf611c279613c704240c0fc8818655d'

def chk_tiingo():
    print('entering chk_tiingo()')
    df = None
    try:
        df = pdr.get_data_tiingo('GOOG', api_key=TIINGO_API_KEY)
    except Exception as  e:
        print ("Error found:", e)
    print(df)    #print(df.loc['Exchange Rate','USD/JPY'])    #print(df.loc['Exchange Rate','USD/INR'])

def chk_av_forex(sym):
    df = None   
    try:
        df = web.DataReader(sym, "av-forex", api_key=ALPHAVANTAGE_API_KEY)
        #print(f'sym:{sym}')
        print (df)
        #df = web.DataReader(["USD/JPY","USD/INR","BTC/USD"], "av-forex", api_key=ALPHAVANTAGE_API_KEY)
        #df = web.get_quote_av(["AAPL", "TSLA"], api_key=ALPHAVANTAGE_API_KEY)       #Check when market is open, else gives error 'Stock Quotes'
    except Exception as  e:
        print ("Error found:", e)
    #print(df.loc['Exchange Rate', sym])    #print(df.loc['Exchange Rate','USD/JPY'])    #print(df.loc['Exchange Rate','USD/INR'])
    return (df.loc['Exchange Rate', sym])

def getQuoteGoogle():
    tickers = ['AAPL', 'MSFT', '^GSPC']
    start_date = '2010-01-01'
    end_date = '2016-12-31'
    panel_data = web.DataReader('INPX', 'google', start_date, end_date)
    web.get_last_iex()
    

def getQuoteYahoo(symbol):
    #symbol = 'GBPINR=X'   #'USDAUD=X'   #'BTCUSD=X'   #'USDINR=X'   #'^NSEI'    #AAPL
    #arrSymbol = ['USDAUD=X','USDAUD=X','BTCUSD=X','USDINR=X','^NSEI','AAPL',]
    panel_data = web.get_quote_yahoo(symbol)        #web.get_quote_yahoo(symbol)
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(panel_data[['price','quoteType','exchangeDataDelayedBy','exchange']])
    #print(panel_data)
    #print(panel_data.columns)
    #print (f"{symbol}: <{panel_data.iloc[0]['price']}>")
    return (panel_data.iloc[0]['price'])

#Provide dataProvider=NSE yahoo=^NSEI, USDINR,
# dataProvider=av-forex symbol=^BTC/USD, USD/INR,
def getLatestRateSingle(dataProvider, symbol):
    if (dataProvider=='yahoo'):
        return getQuoteYahoo(symbol)
    elif (dataProvider=='av-forex'):
        return chk_av_forex(symbol)

def main():
    print('entering main()')
    #chk_av_forex('USD/INR')
    #return
    #chk_tiingo()
    symY = ['^NSEI', 'RELIANCE.NS', 'USDINR=X', 'BTCUSD=X']
    #for sym in symY:
    #    print(f'Values from yahoo   : {sym}:<{getLatestRateSingle("yahoo",sym)}>')
    #getQuoteYahoo('yahoo',symY1)
    symAV = ['USD/JPY', 'USD/INR', 'BTC/USD']
    print(symAV)
    #symAV = ["BTC/USD"]
    for sym in symAV:
        print(f'Values from av-forex: {sym}:<{getLatestRateSingle("av-forex",sym)}>')

if __name__ == "__main__":  
    main()

