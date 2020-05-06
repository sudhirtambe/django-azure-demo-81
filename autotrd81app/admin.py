from django.contrib import admin
from autotrd81app.models import TRADE, PORTFOLIO, REFRATES, GTCORDER

@admin.register(TRADE)
class TRADEAdmin(admin.ModelAdmin):
    list_display = ('strategy','trdDate', 'fill_timestamp', 'transaction_type', 'tradingsymbol', 'quantity', 'average_price', 'ref_symbol', 'ref_rate', 'trade_contra_id')
    ordering = ('-fill_timestamp',)
    search_fields = ('tradingsymbol', 'ref_symbol','strategy')

@admin.register(REFRATES)
class REFRATESAdmin(admin.ModelAdmin):
    list_display = ('timestamp','tradingsymbol', 'price', 'trade_contra_id')
    ordering = ('-timestamp',)
    search_fields = ('tradingsymbol', 'trade_contra_id')

@admin.register(PORTFOLIO)
class PORTFOLIOAdmin(admin.ModelAdmin):
    list_display = ('tradingsymbol','quantity', 'average_price', 'pnl','exchange','is_currency')
    ordering = ('tradingsymbol',)
    search_fields = ('tradingsymbol', 'exchange','is_currency')

@admin.register(GTCORDER)
class GTCORDERAdmin(admin.ModelAdmin):
    list_display = ('gtc_order_date','tradingsymbol', 'price', 'quantity',  'exchange', 'gtc_status')
    ordering = ('-gtc_order_date',)
    search_fields = ('tradingsymbol', 'exchange')

# Register your models here.
#admin.site.register(TRADE)
#admin.site.register(PORTFOLIO)
#admin.site.register(REFRATES)
#admin.site.register(GTCORDER)