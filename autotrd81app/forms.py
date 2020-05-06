from django import forms
from .models import TRADE
from django.forms import inlineformset_factory

class TRADEForm(forms.ModelForm):
    class Meta:
        model = TRADE
        fields = ['transaction_type', 'tradingsymbol', 'quantity', 'average_price', 'trade_id', 'fill_timestamp', 'trdDate',
             'exchange','ref_symbol','ref_rate','asset_type', 'trade_contra_id', 'strategy']

