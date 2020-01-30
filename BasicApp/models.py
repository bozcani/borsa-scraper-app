from django.db import models

# Create your models here.

class StockMarket(models.Model):

    market_id = models.CharField(max_length=10, primary_key=True)
    market_name = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    time_zone = models.IntegerField()
    open_time = models.CharField(max_length=5) # Local time
    close_time = models.CharField(max_length=5) # Local time
    lunch_break = models.CharField(max_length=11) # Local time

    class Meta:
        db_table = 'stock_market_lookup_table'    



class Stock(models.Model):

    stock_symbol = models.CharField(max_length=5, primary_key=True)
    stock_name = models.CharField(max_length=10)
    stock_market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    info_link = models.CharField(max_length=50)

    class Meta:
        db_table = 'stock_lookup_table'           