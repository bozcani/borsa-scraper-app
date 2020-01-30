from django.contrib import admin
from .models import StockMarket, Stock

# Register your models here.
admin.site.register(StockMarket)
admin.site.register(Stock)
