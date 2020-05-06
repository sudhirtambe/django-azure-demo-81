import os
import sys
from pathlib import Path
import django
from django.conf import settings
from django.db import models
PROJECT_ROOT = Path(__file__).parent.parent
#PROJECT_ROOT = Path(__file__)
print('PROJECT_ROOT:', PROJECT_ROOT)
# add project root to sys path
sys.path.append(str(PROJECT_ROOT))
# set up the Django enviroment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autotrd81prj.settings")
django.setup()

import logging
from kiteconnect import KiteTicker
#from autotrd81app import TradeDAO
import TradeDAO

logging.basicConfig(level=logging.DEBUG)

# Initialise
apiKey = 'r0si6b584v698rl1'
accessToken = 'vHsRpZO2k2ok5z117Z4mywUhQovZRVbh'
kws = KiteTicker(apiKey, accessToken)

def on_ticks(ws, ticks):  # noqa
    # Callback to receive ticks.
    #logging.info("Ticks: {}".format(ticks))
    pass

def on_connect(ws, response):  # noqa
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    #ws.subscribe([5633])

    # Set RELIANCE to tick in `full` mode.
    #ws.set_mode(ws.MODE_FULL, [738561])
    logging.info("Successful: on_connect")

def on_order_update(ws, data):  # noqa
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    #print(f'\n\n\ndata:\t{data}')
    if "order_id" in data.keys():
        #print(f"\ndata['order_id']:{data['order_id']}")
        if "status" in data.keys():
            if data['status'] == "NEW" or data['status'] == "OPEN":
                print(f"status:{data['status']}order:{data['order_id']}")
            if data['status'] == "COMPLETE"  or data['status'] == "CANCELLED":
                print(f"status:{data['status']}\norder:{data}")
                #TradeDAO.insertTrade(data)
                TradeDAO.insertKiteMultiTrades(data['order_id'])
    #print(f"data.type:\t{data['type']}")
    #print(f"data.order:\t{data['order']}")
    #if data.status == "COMPLETE" or data.status == "CANCELLED":
    #    print(f'status:{data.status}\norder:{data}')
    #pass
    # Set RELIANCE to tick in `full` mode.
    #ws.set_mode(ws.MODE_FULL, [738561])


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_order_update = on_order_update

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()