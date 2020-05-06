from autotrd81app import models
from django.db.models import Q
import matplotlib.pyplot as plt
import PIL, PIL.Image#, StringIO
from io import StringIO
from matplotlib import pylab
import io
import urllib, base64
from .liverate import getLatestRateSingle
from datetime import datetime, timedelta
import pytz
strFormat = "{:.2f}"
arrINRCurr = ['EURINR', 'GBPINR', 'JPYINR', 'USDINR']
arrUSDCurr = ["AEDUSD", "AUDUSD","CADUSD","CHFUSD","DKKUSD","EURUSD","GBPUSD", "JPYUSD","NOKUSD","NZDUSD"]
def plotValues(pltRef, xyOut):
    if (len(xyOut)>2):
        pltRef.plot(xyOut['ds'].values_list(xyOut['xC']), xyOut['ds'].values_list(xyOut['yC']),   
            linewidth=xyOut.get('linewidth', 0), label=xyOut.get('lbl', 'Blank'), #title='TITLE',  
            marker=xyOut.get('marker', 'o'), markerfacecolor=xyOut.get('mfc', 'c'),markersize=xyOut.get('msize', '1'),
            color=xyOut.get('color', 'w'))
        for x, y in zip(xyOut['ds'].values_list(xyOut['xC']), xyOut['ds'].values_list(xyOut['yC'])):    
            label = strFormat.format(y[0]); 
            pltRef.annotate(label, (x[0],y[0]), textcoords="offset points", xytext=(0,10), ha='center')
    else:
        pltRef.plot(xyOut['x'], xyOut['y'], markersize=12, markerfacecolor='blue', marker='>')
        label = strFormat.format(xyOut['y']); plt.annotate(label, (xyOut['x'],xyOut['y']), xytext=(0,0), textcoords="offset points", ha='left')
    pltRef.legend(loc='upper left')

def getMultiChartImage():
    fig = plt.figure(figsize=(15,6));   arrData= [None] * 4;    arrAx = [None] * 4;     
    arrData[0] = getFutOptData('SS_NIFTY_FUTOPT', "NIFTY", 150, 3, bFut=True, bOpt=True)
    arrData[1] = getFutOptData('SS_CURR_OPT', "USDINR", 0.35, 3, bOpt=True)
    arrData[2] = getFutOptData('SS_REV_CURR_BTC', "BTC", 0, 3)
    arrData[3] = getFutOptData('SS_EQUITY', "BAJFINANCE", 0, 5, yRef='average_price')
    arrAx[0] = plt.subplot(2, 2, 1, title='NIFTY')
    arrAx[1] = plt.subplot(2, 2, 2, title='USDINR')
    arrAx[2] = plt.subplot(2, 2, 3, title='BTC')
    arrAx[3] = plt.subplot(2, 2, 4, title='BAJFINANCE')
    for i in range(len(arrData)):
        for xyOut in arrData[i]: 
            plotValues(arrAx[i], xyOut)
    fig.autofmt_xdate();       fig = plt.gcf();    buf = io.BytesIO();    fig.savefig(buf,format='png')
    buf.seek(0);    string = base64.b64encode(buf.read());    uri =  urllib.parse.quote(string);    plt.close() 
    return uri 


def getChartDataPoints(strat, inSym):
    if strat == "SS_NIFTY_FUTOPT":      arrXYOut = getFutOptData(strat, "NIFTY", 150, 3, bFut=True, bOpt=True)
    elif strat == "SS_CURR_OPT":        arrXYOut = getFutOptData(strat, "USDINR", 0.35, 3, bOpt=True)
    elif strat == "SS_REV_CURR_BTC":    arrXYOut = getFutOptData(strat, inSym, 0, 3)
    elif strat == "SS_EQUITY":          arrXYOut = getFutOptData(strat, inSym, 0, 5, yRef='average_price')
    elif strat == "SS_CURR_FUT_PAIRS":  arrXYOut = getFutOptData(strat, inSym, 0, 5, yRef='average_price', bFut=True)
    elif strat == "SS_REV_CURR_PAIRS":  arrXYOut = getFutOptData(strat, inSym, 0, 3)
    return arrXYOut

def getSingleChartImage(strat, inSym):
    if (strat == "SS_CURR_FUT_PAIRS"):
        arrXYOut = []
        for sym in arrINRCurr:            arrXYOut = getChartDataPoints(strat, sym)
        arrXYOut += getRefDataForStrat(strat)
    if (strat == "SS_REV_CURR_PAIRS"):
        arrXYOut = []
        for sym in arrUSDCurr:            arrXYOut = getChartDataPoints(strat, sym)[0:3]
        arrXYOut += getRefDataForStrat(strat)
    else:
        arrXYOut = getChartDataPoints(strat, inSym)
    fig = plt.figure(figsize=(15,6))
    for xyOut in arrXYOut:
        plotValues(plt, xyOut)
    fig.autofmt_xdate();    plt.legend(loc='upper left');   fig = plt.gcf();    buf = io.BytesIO();    fig.savefig(buf,format='png')
    buf.seek(0);    string = base64.b64encode(buf.read());    uri =  urllib.parse.quote(string);    plt.close() 
    return uri 

def getRefDataForStrat(strat):
    if strat == "SS_CURR_FUT_PAIRS":        arrSym = arrINRCurr
    elif strat == "SS_REV_CURR_PAIRS": arrSym = arrUSDCurr
    arrOut = []
    for sym in arrSym:
        arrOut += getRefDataForSymbol(sym)
    return arrOut

def getRefDataForSymbol(inSym, posCount=3):
    qsPos = models.REFRATES.objects.filter(tradingsymbol=inSym).order_by('-timestamp')[:posCount]
    arrOut = []
    ds = {'ds': qsPos, 'xC':'timestamp', 'yC':'price', 'lbl':'RefData', 'linewidth':'1', 'color':'grey', 'msize':1};    arrOut.append(ds)
    return arrOut

'''Returns an array of x, and y in below format[{title: posLong, x:[datetimes], y: [rates], marker='^', color=green, annotate=True, markersize=12, markerfacecolor='green'},   {title: posShort, x:[datetimes], y: [rates], marker='v', color=green},  {title: insLong}, {title: insShort}, {title: live}] '''
def getFutOptData(strat, inSym, posPrice, posCount=3, bFut=False, bOpt=False, yRef='ref_rate'):
    if bFut and bOpt:
        qObj = (Q(tradingsymbol__endswith='FUT') & Q(transaction_type='BUY')) | (Q(tradingsymbol__endswith='PE') & Q(transaction_type='SELL'))
        qsPosLong = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__gte=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
        qObj = (Q(tradingsymbol__endswith='FUT') & Q(transaction_type='SELL')) | (Q(tradingsymbol__endswith='CE') & Q(transaction_type='SELL'))
        qsPosShort = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__gte=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
    elif bOpt:
        qObj = (Q(tradingsymbol__endswith='PE') & Q(transaction_type='SELL'))
        qsPosLong = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__gte=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
        qObj = (Q(tradingsymbol__endswith='CE') & Q(transaction_type='SELL'))
        qsPosShort = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__gte=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
    elif bFut:
        qObj = (Q(tradingsymbol__endswith='FUT') & Q(transaction_type='BUY')) 
        qsPosLong = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__gte=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
        qObj = (Q(tradingsymbol__endswith='FUT') & Q(transaction_type='SELL'))
        qsPosShort = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__gte=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
    elif not (bFut or bOpt):
        qsPosLong = models.TRADE.objects.filter(strategy=strat).filter(tradingsymbol=inSym).filter(transaction_type="BUY").order_by('-fill_timestamp')[:posCount]
        qsPosShort = models.TRADE.objects.filter(strategy=strat).filter(tradingsymbol=inSym).filter(transaction_type="SELL").order_by('-fill_timestamp')[:posCount]
    arrOut = []
    ds = {'ds': qsPosLong, 'xC':'fill_timestamp', 'yC':yRef, 'lbl':'posLong', 'marker':'^', 'mfc':'green', 'msize':12};    arrOut.append(ds)
    ds = {'ds': qsPosShort,'xC':'fill_timestamp', 'yC':yRef, 'lbl':'posShort','marker':'v', 'mfc':'red', 'msize':12};  arrOut.append(ds)
    print(ds)
    if bOpt:
        qObj = (Q(tradingsymbol__endswith='CE') & Q(transaction_type='BUY'))
        qsInsLong = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__lt=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
        qObj = (Q(tradingsymbol__endswith='PE') & Q(transaction_type='BUY'))
        qsInsShort = models.TRADE.objects.filter(strategy=strat).filter(ref_symbol=inSym).filter(average_price__lt=posPrice).filter(qObj).order_by('-fill_timestamp')[:posCount]
        ds = {'ds': qsInsLong, 'xC':'fill_timestamp', 'yC':yRef, 'lbl':'insLong', 'marker':'o', 'mfc':'lime', 'msize':6};    arrOut.append(ds)
        ds = {'ds': qsInsShort,'xC':'fill_timestamp', 'yC':yRef, 'lbl':'insShort','marker':'o', 'mfc':'salmon', 'msize':6};  arrOut.append(ds)
    if   strat == "SS_NIFTY_FUTOPT"  :     curRate = getLatestRateSingle('yahoo', '^NSEI')
    elif strat == "SS_CURR_OPT" :     curRate = getLatestRateSingle('yahoo', 'USDINR=X')
    elif strat == "SS_REV_CURR_BTC"    :     curRate = getLatestRateSingle('yahoo', 'BTCUSD=X')
    elif strat == "SS_CURR_FUT_PAIRS" :     
        curRate = getLatestRateSingle('yahoo', inSym[0:6]+'=X')
        if curRate < 1: curRate *= 100
    elif strat == "SS_EQUITY"    :     
        curRate = getLatestRateSingle('yahoo', inSym+'.NS')
        print(f'inSym: {inSym} curRate:{curRate}')
    elif strat == "SS_REV_CURR_PAIRS"    :     
        curRate = getLatestRateSingle('yahoo', inSym+'USD=X')
        print(f'inSym: {inSym} curRate:{curRate}')
    currTime = pytz.utc.localize(datetime.utcnow()) 
    ds = {'x': [currTime], 'y':curRate};    print(ds);  arrOut.append(ds)
    return arrOut
