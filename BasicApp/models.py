from django.db import models

# Create your models here.

class StockMarket(models.Model):

    market_id = models.CharField(max_length=20, primary_key=True)
    market_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    time_zone = models.CharField(max_length=10)
    open_time = models.CharField(max_length=50) # Local time
    close_time = models.CharField(max_length=50) # Local time
    lunch_break = models.CharField(max_length=50) # Local time

    class Meta:
        db_table = 'stock_market_lookup_table'    

    def __str__(self):
        return "<StockMarket Object> market_id {}".format(self.market_id)


class Stock(models.Model):

    stock_symbol = models.CharField(max_length=20, primary_key=True)
    stock_name = models.CharField(max_length=200)
    stock_market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    info_link = models.CharField(max_length=500)

    class Meta:
        db_table = 'stock_lookup_table'           

    def __str__(self):
        return "<Stock Object> stock_symbol {}, stock_name {}, stock_market {}".format(self.stock_symbol, self.stock_name, self.stock_market.market_id)

class LookupTablesUpdateStatus(models.Model):
    table_name = models.CharField(max_length=40, primary_key=True)    
    last_update = models.TimeField(auto_now=True)
    source = models.CharField(max_length=100)

class StockDataLastUpdate(models.Model):
    stock_market = models.OneToOneField(Stock, on_delete=models.CASCADE, primary_key=True)
    last_update = models.DateTimeField()      