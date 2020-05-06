import csv, io
from django.shortcuts import render
from autotrd81app import models
from django.http import HttpResponse, Http404, HttpResponseRedirect
import pandas as pd
import matplotlib.pyplot as plt
import PIL, PIL.Image#, StringIO
from io import StringIO
from matplotlib import pylab
import io
import urllib, base64
from datetime import datetime, timedelta
from .liverate import getLatestRateSingle
import pytz
from django.db.models import Q
from .forms import TRADEForm
from django.urls import reverse
from django.views import generic
from autotrd81app.UtilJson import getNestedConfigItem
from autotrd81app.ConfJSONLoader import ConfJSONLoader
from autotrd81app import currency, PortfolioDAO, TradeDAO, ChartDataDAO
from autotrd81app.kc import  KiteInteractionDAO
from django.views.generic.list import ListView
import logging

logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def getMultiChartImage(request):
    uri = ChartDataDAO.getMultiChartImage
    return render(request,'getChartImage.html',{'data':uri})
        
def list_trade(request):
    qs = TRADE.objects.filter(ref_symbol="NIFTY") .order_by('-fill_timestamp')[:5]
    print(qs)
    q = qs.values('fill_timestamp','ref_symbol','average_price','tradingsymbol','ref_rate')
    print(q)
    #df = pd.DataFrame.from_records(q, columns=("average_price","fill_timestamp")).set_index('fill_timestamp')
    df = pd.DataFrame.from_records(q).set_index('fill_timestamp')
    #df['fill_timestamp'] = df['fill_timestamp'].dt.date
    print(df)
    df.ref_rate=pd.to_numeric(df.ref_rate)
    df['ref_rate'].plot()
    #plt.show()
    return HttpResponse('previous request completed')

def getChartImage(request, strat, inSym):
    uri = ChartDataDAO.getSingleChartImage(strat, inSym)
    return render(request,'getChartImage.html',{'data':uri})

def newSingleTrade(request, strat, transType):
    if request.method == 'POST':
        try:
            form = TRADEForm(request.POST)
            trade = form.save(commit=False)
            #trade.save()
            ordId = KiteInteractionDAO.placeOrder(trade)
            print(f'ordId:{ordId}')
            logging.info('views::newSingleTrade:' + ordId)
            if ordId is not None:
                return render(request, 'confirmation.html', {'success': trade, 'msg':ordId})
        except Exception as e:
            raise Http404('newSingleTrade Failed for strategy:'+strat + ' and transType:' + transType + 'error ' + str(e))
    else:
        mT = TradeDAO.getDefaultFormParams(strat, transType)
        form = TRADEForm(initial={'transaction_type':mT.transaction_type, 'strategy':mT.strategy, 'exchange':mT.exchange, 
            'asset_type':mT.asset_type, 'quantity':mT.quantity, 'ref_symbol': mT.ref_symbol, 'ref_rate': mT.ref_rate})
    return render(request, 'newTrade.html', {'form': form})

def newCrossTrade(request, strat):
    if request.method == 'POST':
        formBuy   = TRADEForm(request.POST, prefix='formBuy')       ; print(f'formBuy.tradingsymbol:{formBuy.instance.tradingsymbol}')
        if not formBuy.is_valid():
            print('formBUy is not Valid')
            print(formBuy.errors)
            raise Http404('formBUy is not Valid for strat:'+strat)
        formSell  = TRADEForm(request.POST, prefix='formSell')      #; print(f'formSell:{formSell}')
        tradeBuy  = formBuy.save(commit=False)                      #; print(f'tradeBuy:{tradeBuy}')
        tradeSell = formSell.save(commit=False)                     #; print(f'tradeSell:{tradeSell}')
        if strat in ['SS_EQUITY', 'SS_CURR_FUT_PAIRS', 'SS_CURR_OPT', 'SS_NIFTY_FUTOPT']:
            ordId1 = KiteInteractionDAO.placeOrder(tradeBuy)
            ordId2 = KiteInteractionDAO.placeOrder(tradeSell)
            logging.warn(f'Kite Executed two orders: ordId1:{ordId1}  ordId2:{ordId2}')
        else:
            tradeBuy.save()
            tradeSell.save()
        PortfolioDAO.addTradeToPF(tradeBuy)
        PortfolioDAO.addTradeToPF(tradeSell)
        currency.insertCurrLTPs(strat, formBuy.cleaned_data['trade_contra_id'])
        return render(request, 'confirmation.html', {'success': formBuy, 'msg':formSell})
    else:
        mT = TradeDAO.getDefaultFormParams(strat,   None)
        formBuy = TRADEForm(prefix='formBuy', initial={'transaction_type':'BUY', 'strategy':mT.strategy, 'exchange':mT.exchange, 'asset_type':mT.asset_type, 
            'quantity':mT.quantity, 'ref_symbol': mT.ref_symbol, 'ref_rate': mT.ref_rate, 'trade_contra_id': mT.trade_contra_id})
        formSell = TRADEForm(prefix='formSell', initial={'transaction_type':'SELL', 'strategy':mT.strategy, 'exchange':mT.exchange, 'asset_type':mT.asset_type, 
            'quantity':mT.quantity, 'ref_symbol': mT.ref_symbol, 'ref_rate': mT.ref_rate, 'trade_contra_id': mT.trade_contra_id})
        args = {'formBuy':formBuy, 'formSell':formSell}
        return render(request, 'newCrossTrade.html', args)

def kiteTradesAsDBObjects():
    trades = KiteInteractionDAO.getTradesForDay()
    objTRADEList = []
    for trade in trades:
        newTrdObj = TradeDAO.insertKiteTradeAsDBObj(trade)
        objTRADEList.append(newTrdObj)
    return objTRADEList

class IndexView(generic.TemplateView):
    template_name = 'base.html'

class TradeListView(ListView):
    model = models.TRADE
    template = 'trade_list.html'
    def get_context_data(self, **kwargs):
        context = super(TradeListView, self).get_context_data(**kwargs)
        context['trade_list'] = kiteTradesAsDBObjects()
        return context

def upload_trade(request):
    template = 'trade_upload.html'
    prompt = {'order': 'order of csv check models.py::TRADE'}
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['fileipcsv']
    print(f'csv_file: {csv_file}')
    data_set = csv_file.read().decode('UTF-8')
    io_string = StringIO(data_set)
    print(io_string)
    next(io_string)
    try:
        for column in csv.reader(io_string, delimiter=';', quotechar='|'):
            print('column:', column)
            _, created = models.TRADE.objects.update_or_create(
                transaction_type=column[0], tradingsymbol=column[1], quantity=column[2], average_price=column[3], trade_id=column[5],
                fill_timestamp=column[7], exchange=column[8], asset_type=column[12], strategy=column[14], 
                order_id=None if column[4]==' ' else column[4], orderTimestamp=None if column[6]=='' else column[6],
                ref_symbol=None if column[9]==' ' else column[9], ref_rate=None if column[10]=='' else column[10],
                exchange_order_id=None if column[11]==' ' else column[11],trade_contra_id=None if column[13]=='' else column[13],
                trdDate=None if column[15]=='' else column[15]
            )
    except Exception as e:
        print(f'error occurred: {e}')
    context = {}
    return render(request, template, context)
