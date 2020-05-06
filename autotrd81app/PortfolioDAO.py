from autotrd81app.models import TRADE, PORTFOLIO
from django.core.exceptions import ObjectDoesNotExist

def addTradeToPF(inTrd):
    trdSym = inTrd.tradingsymbol
    try:
        pfObj = PORTFOLIO.objects.get(tradingsymbol=trdSym)
        print(f'Original Object pfObj:{pfObj}')
        # Modify quantity, average_price and pnl
        oldQty = pfObj.quantity
        oldRate = pfObj.average_price
        oldPnl = pfObj.pnl
        newRate = inTrd.average_price
        newPnl = oldPnl
        newQty = inTrd.quantity
        if inTrd.transaction_type=="BUY":                       ## Modify quantity, average_price
            if pfObj.is_currency:      
                pfObj.average_price += newRate
            else:
                pfObj.quantity = oldQty + inTrd.quantity            
                if (oldQty + newQty) != 0:          newRate = float( (oldRate * oldQty) + (newRate * newQty)) / (oldQty + newQty)
                else:                               newRate = 0.0
                pfObj.average_price = newRate
        elif inTrd.transaction_type=="SELL":                    ## Modify quantity, average_price, pnl
            if pfObj.is_currency:      
                pfObj.average_price -= newRate
            else:
                pfObj.quantity = oldQty - inTrd.quantity
                newRate = ( (oldRate * oldQty) - (newRate * newQty)) / (oldQty + newQty)
                newPnl = float(oldPnl) + float(newRate - oldRate) * float(newQty)
                pfObj.pnl = newRate
                pfObj.average_price = newRate
        print(f'Before Updating Existing row in DB pfObj:{pfObj}')
        pfObj.save()
    except ObjectDoesNotExist:
        bCurr = False
        if len(inTrd.tradingsymbol) == 3:   bCurr = True
        newPFObj = PORTFOLIO(tradingsymbol=inTrd.tradingsymbol, quantity=inTrd.quantity, average_price=inTrd.average_price, 
            pnl=0, exchange=inTrd.exchange, is_currency=bCurr)
        print(f'Before Storing in DB as New Object pfObj:{newPFObj}')
        newPFObj.save()
