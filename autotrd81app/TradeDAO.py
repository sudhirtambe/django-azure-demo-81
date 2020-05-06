import django
from django.db.models import Max
from autotrd81app import models
from autotrd81app import UtilJson
from autotrd81app import currency
from autotrd81app.ConfJSONLoader import ConfJSONLoader   
from autotrd81app.kc import KiteInteractionDAO

def insertKiteMultiTrades(ordId):
    kiteTrades = KiteInteractionDAO.getTradeByOrdId(ordId)
    for trade in kiteTrades:
        insertKiteTradeAsDBObj(trade)

def insertKiteTradeAsDBObj(trd):
    #print(f'insertKiteTradeAsDBObj::trd : {trd}')
    print(f"Entering insertKiteTradeAsDBObj with trdSym: {trd['tradingsymbol']}")
    assetType, strat, refSym, refRate, trdContraId = ConfJSONLoader.getTrdSymRefData(trd['tradingsymbol'], trd['exchange'])
    print(f'received refSym:{refSym} refRate:{refRate} trdContraId:{trdContraId}')
    newTrd = models.TRADE(transaction_type=trd['transaction_type'], tradingsymbol=trd['tradingsymbol'], quantity=trd['quantity'],
        average_price=trd['average_price'], order_id=trd['order_id'], trade_id=trd['trade_id'],
        fill_timestamp=trd['fill_timestamp'], exchange=trd['exchange'],
        exchange_order_id=trd['exchange_order_id'], asset_type=assetType, strategy=strat    )
    if refSym is not None:      newTrd.ref_symbol = refSym
    if refRate >= 0:            newTrd.ref_rate = refRate
    if trdContraId >= 0:        newTrd.trade_contra_id = trdContraId
    #print(f'Before saving to db newTrd:{newTrd} refSym::{newTrd.refSym} refRate::{newTrd.refRate} ')
    newTrd.save()
    return newTrd

def getDefaultFormParams(strat, transType):
    confStrat = ConfJSONLoader.get_instance()
    exchange = UtilJson.getNestedConfigItem(confStrat.dictConf['confStrat'], strat,'EXCHANGE')
    asset_type = UtilJson.getNestedConfigItem(confStrat.dictConf['confStrat'],  strat,'ASSET_TYPE')
    quantity = UtilJson.getNestedConfigItem(confStrat.dictConf['confStrat'],  strat,'DEFAULT_QTY')
    ref_symbol = UtilJson.getNestedConfigItem(confStrat.dictConf['confStrat'],  strat,'REF', 'REF_SYM')
    print(f'strat: {strat} ref_symbol: {ref_symbol}')
    if ref_symbol is not None and ref_symbol != "" and ref_symbol != "SELF":
        ref_rate = currency.getSingleQuoteYahoo(ref_symbol)
    else: ref_rate=0
    trade_contra_id = models.TRADE.objects.aggregate(Max('trade_contra_id'))['trade_contra_id__max'] + 1
    print(f'trade_contra_id: {trade_contra_id}')
    trd = models.TRADE(exchange=exchange, asset_type=asset_type, quantity=quantity, ref_symbol=ref_symbol, ref_rate=ref_rate, 
        transaction_type =transType, strategy=strat, trade_contra_id=trade_contra_id)
    print(f'exchange:{exchange} asset_type:{asset_type} defQty:{quantity} ')
    return trd
