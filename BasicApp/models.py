from django.db import models

# Create your models here.

class StockMarket(models.Model):

    market_id = models.CharField(max_length=10, primary_key=True)
    market_name = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    time_zone = models.IntegerField()
    open_time = models.CharField(max_length=5) # Local time
    close_time = models.CharField(max_length=5) # Local time
    lunch_break = models.CharField(max_length=11) # Local time

    class Meta:
        db_table = 'stock_market_lookup_table'    

    def __str__(self):
        return "<StockMarket Object> market_id {}".format(self.market_id)


class Stock(models.Model):

    stock_symbol = models.CharField(max_length=5, primary_key=True)
    stock_name = models.CharField(max_length=30)
    stock_market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    info_link = models.CharField(max_length=100)

    class Meta:
        db_table = 'stock_lookup_table'           