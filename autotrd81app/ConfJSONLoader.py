import json
from autotrd81app import  models
#import UtilJson, models
from autotrd81app.liverate import getLatestRateSingle
from django.db.models import Max

#dictConf = {'confKite':''}

class ConfJSONLoader:
    __instance__ = None
    dictConf = {'confKite':'', 'confStrat':''}

    @staticmethod
    def loadAllJSONConf(self):
        print('Entering ConfJSONLoader::loadAllJSONConf')
        for key in self.dictConf.keys():
            #print(key)
            with open('./autotrd81prj/static/'+key+'.json', 'r') as f:
                self.dictConf[key] = json.load(f)
        print("KITE_ACCESS_TOKEN:" , self.dictConf.get('confKite',{}).get('KITE_ACCESS_TOKEN',None))
    
    def __init__(self):
        if ConfJSONLoader.__instance__ is None:
            ConfJSONLoader.__instance__ = self
            ConfJSONLoader.loadAllJSONConf(self)
        else:
            raise Exception("You cannot create another SingletonGovt class")

    @staticmethod
    def get_instance():
        """ Static method to fetch the current instance.
        """
        if not ConfJSONLoader.__instance__:
            ConfJSONLoader()
        return ConfJSONLoader.__instance__

    #Given tradingSymbol and exchange
    # return data: assetType, strat, refSym, refRate, trdContraId
    # e.g. INFY, NSE => assetType:EQ, strat:SS_EQUITY, refSym:None, refRate:-1, trdContraId:-1
    # USDINR20MAYFUT, CDS => CFO, SS_CURR_FUT_PAIRS, refSym:USDINR, refRate:Rate, tCId: max(contraId)       [*INR*FUT]
    # USDINR20MAY7800CE, CDS => CFO, SS_CURR_OPT, USDINR, refRate:Rate(USDINR) tCId: -1                     [USDINR*E]
    # NIFTY20MAYFUT|NIFTY20MAY9000PE, NFO => NFO, SS_NIFTY_FUTOPT, NIFTY 50, rate(NIFTY50), -1              [NIFTY*]
    # SS_REV_CURR_PAIRS
    # SS_REV_CURR_BTC
    @staticmethod
    def getTrdSymRefData(trdSym, exch):
        outAssetType, outStrat, outRefSym = None, None, None
        outRefRate, outContraId = -1, -1
        if exch == "NSE" or exch=="BSE":
            outAssetType = "EQ";    outStrat="SS_EQUITY"
        elif exch == "NFO":
            outAssetType = "NFO";    outStrat="SS_NIFTY_FUTOPT"           
            outRefSym="NIFTY";      outRefRate = getLatestRateSingle('yahoo', '^NSEI')
        elif exch == "CDS":
            if trdSym.endswith("FUT"):
                outAssetType = "CFO";    outStrat="SS_CURR_FUT_PAIRS"
                outRefSym=trdSym[:6];      outRefRate = getLatestRateSingle('yahoo', outRefSym+"=X")
                outContraId = models.TRADE.objects.aggregate(Max('trade_contra_id'))['trade_contra_id__max']
                try:                                
                    existingRec = models.TRADE.objects.get(trade_contra_id=outContraId, tradingSymbol__endswith="FUT")
                except models.TRADE.DoesNotExist:                   outContraId += 1
                except models.TRADE.MultipleObjectsReturned:        outContraId += 1
            elif trdSym.endswith("E"):
                outAssetType = "CFO";    outStrat="SS_CURR_OPT"    
                outRefSym=trdSym[:6];      outRefRate = getLatestRateSingle('yahoo', outRefSym+"=X")
        return outAssetType, outStrat, outRefSym, outRefRate, outContraId