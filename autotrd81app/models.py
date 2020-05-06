from django.db import models
from datetime import datetime
import django
from django.utils import timezone

# Create your models here.
class TRADE(models.Model):
    transaction_type = models.CharField(max_length=4, choices=(("BUY", "BUY"),("SELL","SELL")))
    tradingsymbol = models.CharField(max_length=24)
    quantity = models.PositiveSmallIntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=4)
    order_id = models.CharField(max_length=16, blank=True)
    trade_id = models.CharField(max_length=8, blank=True)
    orderTimestamp  = models.DateTimeField (null=True, blank=True)
    fill_timestamp  = models.DateTimeField (default=django.utils.timezone.now)
    trdDate = models.DateField(default=timezone.now)
    exchange = models.CharField(max_length=3, 
        choices=(("BSE", "BSE"),("NSE","NSE"),("NFO","NFO"),("CDS","CDS"),("REV","REV"),("OTH","OTH")))
    ref_symbol = models.CharField(max_length=24, blank=True)
    ref_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    exchange_order_id = models.CharField(max_length=16, blank=True)
    asset_type = models.CharField(max_length=3, 
        choices=(("EQ", "EQ"),("NFO","NFO"),("CFO","CFO"),("CUR","CUR"),("DIG","DIG"),("OTH","OTH")))
    trade_contra_id = models.PositiveSmallIntegerField(null=True, blank=True)
    strategy = models.CharField(max_length=20, 
        choices=(("SS_EQUITY", "SS_EQUITY"),("SS_CURR_FUT_PAIRS","SS_CURR_FUT_PAIRS"),("SS_CURR_OPT","SS_CURR_OPT"),
            ("SS_NIFTY_FUTOPT","SS_NIFTY_FUTOPT"),("SS_REV_CURR_PAIRS","SS_REV_CURR_PAIRS"),("SS_REV_CURR_BTC","SS_REV_CURR_BTC"),("OTH","OTH")))
    #position_type = models.CharField(max_length=5, choices=(("LONG", "LONG"),("SHORT","SHORT")))
    def __str__(self):
        return str(self.fill_timestamp) + " " + self.asset_type + ":" + self.transaction_type + " " + self.tradingsymbol + ":" + str(self.quantity) + "@" + str(self.average_price)
    def get_fields(self):
        return [(field, field.value_to_string(self)) for field in TRADE._meta.fields]

class PORTFOLIO(models.Model):
    tradingsymbol = models.CharField(max_length=24, unique=True)
    quantity = models.SmallIntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=4)
    pnl = models.FloatField(null=True)
    exchange = models.CharField(max_length=3, 
        choices=(("BSE", "BSE"),("NSE","NSE"),("NFO","NFO"),("CDS","CDS"),("REV","REV"),("OTH","OTH")))
    is_currency = models.BooleanField()

class REFRATES(models.Model):
    tradingsymbol = models.CharField(max_length=24)
    timestamp  = models.DateTimeField ()
    price = models.DecimalField(max_digits=10, decimal_places=4)
    trade_contra_id = models.PositiveSmallIntegerField()


class GTCORDER(models.Model):
    tradingsymbol = models.CharField(max_length=24)
    exchange = models.CharField(max_length=3, 
        choices=(("BSE", "BSE"),("NSE","NSE"),("NFO","NFO"),("CDS","CDS"),("REV","REV"),("OTH","OTH")))
    transaction_type = models.CharField(max_length=4, choices=(("BUY", "BUY"),("SELL","SELL")))
    quantity = models.SmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    price_trigger = models.DecimalField(max_digits=10, decimal_places=4)
    price_trigger_gtc = models.DecimalField(max_digits=10, decimal_places=4)
    orderTimestamp  = models.DateTimeField (null=True)
    fill_timestamp  = models.DateTimeField (null=True)
    date_activation = models.DateField()
    date_expiry = models.DateField()
    gtc_status = models.CharField(max_length=10, default='NEW',
        choices=(("NEW", "NEW"),("ORDERED","ORDERED"),("CANCELLED","CANCELLED"),("COMPLETED","COMPLETED"),("REV","REV"),("OTH","OTH")))
    cancel_other_on_comp = models.PositiveSmallIntegerField(null=True)
    trigger_other_on_comp = models.PositiveSmallIntegerField(null=True)
    dependent_on_completion = models.PositiveSmallIntegerField(null=True)
    gtc_order_date = models.DateField(auto_now_add=True)



