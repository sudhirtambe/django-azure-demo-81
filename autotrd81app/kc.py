import logging
from kiteconnect import KiteConnect
from autotrd81app.ConfJSONLoader import ConfJSONLoader
from autotrd81app import UtilJson, models
from autotrd81app import KiteUtil

logging.basicConfig(level=logging.DEBUG)
class KiteInteractionDAO:
    @staticmethod
    def placeOrder(ord):
        logging.info(f'About to place order: {ord}')
        kite = KiteSingleton.get_instance()
        logging.info(f'KiteInteractionDAO::placeOrder kite {kite}')
        inProduct = "CNC"       if ord.exchange=="NSE"      else "NRML"
        inVariety = "regular"   if KiteUtil.isMktOpen()     else "amo"
        logging.warn(f'about to order:{ord}')
        try:
            ordId = kite.place_order(tradingsymbol=ord.tradingsymbol,  exchange=ord.exchange, transaction_type=ord.transaction_type,
                                quantity=ord.quantity, price=ord.average_price,    order_type="LIMIT", variety=inVariety, product=inProduct)
            logging.warn(f'Order placed for orderId: {ordId}')
        except Exception as e:
            logging.error("error received"); logging.error( e); raise e
        return ordId
    
    @staticmethod
    def getTradeByOrdId(ordId):
        kite = KiteSingleton.get_instance()
        multiTrds = kite.order_trades(ordId)
        return multiTrds
        
    @staticmethod
    def getTradesForDay():
        kite = KiteSingleton.get_instance()
        return kite.trades()
        
class KiteSingleton:
    __instance__ = None
    kite = None

    def __init__(self):
        print('KiteSingleton::__init__()')
        if KiteSingleton.__instance__ is None:
            KiteSingleton.__instance__ = self
            KiteSingleton.loadKiteObj()
        else:
            raise Exception("You cannot create another SingletonGovt class")

    @staticmethod
    def get_instance():
        print('KiteSingleton::get_instance()')
        if not KiteSingleton.__instance__:
            KiteSingleton()
        print('get_instance::kite', KiteSingleton.kite)
        return KiteSingleton.kite

    @staticmethod
    def loadKiteObj():
        print('KiteSingleton::loadKiteObj()')
        confStrat = ConfJSONLoader.get_instance()
        apiKey = UtilJson.getNestedConfigItem(confStrat.dictConf['confKite'], 'apiKey')
        kiteAccessToken = UtilJson.getNestedConfigItem(confStrat.dictConf['confKite'], 'KITE_ACCESS_TOKEN')
        print(f'Trying to connect kite with api_key:<{apiKey}> and KITE_ACCESS_TOKEN:<{kiteAccessToken}>')
        KiteSingleton.kite=KiteConnect(apiKey)
        KiteSingleton.kite.set_access_token(kiteAccessToken)
        print('kiteObject received:', KiteSingleton.kite)
