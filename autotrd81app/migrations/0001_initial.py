# Generated by Django 2.1.15 on 2020-04-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GTCORDER',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradingsymbol', models.CharField(max_length=24)),
                ('exchange', models.CharField(choices=[('BSE', 'BSE'), ('NSE', 'NSE'), ('NFO', 'NFO'), ('CDS', 'CDS'), ('REV', 'REV'), ('OTH', 'OTH')], max_length=3)),
                ('transaction_type', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=4)),
                ('price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('price_trigger', models.DecimalField(decimal_places=4, max_digits=10)),
                ('price_trigger_gtc', models.DecimalField(decimal_places=4, max_digits=10)),
                ('orderTimestamp', models.DateTimeField(null=True)),
                ('fill_timestamp', models.DateTimeField(null=True)),
                ('date_activation', models.DateField()),
                ('date_expiry', models.DateField()),
                ('gtc_tatus', models.CharField(choices=[('NEW', 'NEW'), ('ORDERED', 'ORDERED'), ('CANCELLED', 'CANCELLED'), ('COMPLETED', 'COMPLETED'), ('REV', 'REV'), ('OTH', 'OTH')], max_length=10)),
                ('cancel_other_on_comp', models.PositiveSmallIntegerField(null=True)),
                ('trigger_other_on_comp', models.PositiveSmallIntegerField(null=True)),
                ('dependent_on_completion', models.PositiveSmallIntegerField(null=True)),
                ('gtc_order_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PORTFOLIO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradingsymbol', models.CharField(max_length=24, unique=True)),
                ('quantity', models.SmallIntegerField()),
                ('average_price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('pnl', models.FloatField(null=True)),
                ('exchange', models.CharField(choices=[('BSE', 'BSE'), ('NSE', 'NSE'), ('NFO', 'NFO'), ('CDS', 'CDS'), ('REV', 'REV'), ('OTH', 'OTH')], max_length=3)),
                ('is_currency', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='REFRATES',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tradingsymbol', models.CharField(max_length=24)),
                ('timestamp', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('trade_contra_id', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TRADE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], max_length=4)),
                ('tradingsymbol', models.CharField(max_length=24)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('average_price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('order_id', models.CharField(blank=True, max_length=16)),
                ('trade_id', models.CharField(blank=True, max_length=8)),
                ('orderTimestamp', models.DateTimeField(blank=True, null=True)),
                ('fill_timestamp', models.DateTimeField()),
                ('exchange', models.CharField(choices=[('BSE', 'BSE'), ('NSE', 'NSE'), ('NFO', 'NFO'), ('CDS', 'CDS'), ('REV', 'REV'), ('OTH', 'OTH')], max_length=3)),
                ('ref_symbol', models.CharField(blank=True, max_length=24)),
                ('ref_rate', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('exchange_order_id', models.CharField(blank=True, max_length=16)),
                ('asset_type', models.CharField(choices=[('EQ', 'EQ'), ('NFO', 'NFO'), ('CFO', 'CFO'), ('CUR', 'CUR'), ('DIG', 'DIG'), ('OTH', 'OTH')], max_length=3)),
                ('trade_contra_id', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('strategy', models.CharField(choices=[('SS_EQUITY', 'SS_EQUITY'), ('SS_CURR_FUT_PAIRS', 'SS_CURR_FUT_PAIRS'), ('SS_CURR_OPT', 'SS_CURR_OPT'), ('SS_NIFTY_FUTOPT', 'SS_NIFTY_FUTOPT'), ('SS_REV_CURR_PAIRS', 'SS_REV_CURR_PAIRS'), ('SS_REV_CURR_BTC', 'SS_REV_CURR_BTC'), ('OTH', 'OTH')], max_length=20)),
            ],
        ),
    ]
