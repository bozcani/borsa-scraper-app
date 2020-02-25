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


class StockDataLastUpdate(models.Model):
    stock_market = models.OneToOneField(Stock, on_delete=models.CASCADE, primary_key=True)
    last_update = models.DateTimeField()  

    class Meta:
        db_table = 'StockDataLastUpdate_table'

    def __str__(self):
        return "<StockDataLastUpdate Object> stock_market {}, last_update {}".format(self.stock_market.market_id, self.last_update)

class CookieCrumbPair(models.Model):
    cookie = models.BinaryField()
    crumb = models.CharField(max_length=20)
    saved_date = models.DateTimeField()

    class Meta:
        db_table = 'CookieCrumbPair_table'

    def __str__(self):
        return "<CookieCrumbPair Object> cookie is binary, crumb {}, saved_date {}".format(self.crumb, self.saved_date)



class OHLCV(models.Model):
    date = models.DateField()
    stock_symbol = models.CharField(max_length=20)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        db_table = 'OHLCV_table'

    def __str__(self):
        return "<OHLCV Object> date {}, stock_symbol {}, open {}, high {}, low {}, close {}, volume {}".format(self.date, 
                                                                                                                self.stock_symbol, 
                                                                                                                self.open, 
                                                                                                                self.high,
                                                                                                                self.low,
                                                                                                                self.close,
                                                                                                                self.volume)    


                                                                                                                