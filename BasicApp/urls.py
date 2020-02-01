from django.urls import path
from django.contrib import admin

from . import views


app_name = 'BasicApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('add_stock_market_result', views.add_stock_market_result, name='add_stock_market_result'),
    path('stock_market/<str:market_id>/', views.stock_market, name='stock_market'),
]
