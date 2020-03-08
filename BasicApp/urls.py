from django.urls import path
from django.contrib import admin

from . import views


app_name = 'BasicApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('add_stock_market_result/', views.add_stock_market_result, name='add_stock_market_result'),
    path('stock_market/<str:market_id>/', views.stock_market, name='stock_market'),
    path('stock_history/<str:stock_symbol>/', views.stock_history, name='stock_history'),
    path('delete_stock_market/<str:market_id>/', views.delete_stock_market, name='delete_stock_market'),
    path('data_manager/', views.data_manager, name='data_manager'),
    path('data_update_status/', views.data_update_status, name='data_update_status'),
    path('update_stock_market_lookup_table/', views.update_stock_market_lookup_table, name='update_stock_market_lookup_table'),
    path('update_stock_lookup_table/', views.update_stock_lookup_table, name='update_stock_lookup_table'),
    path('delete_stock_market_lookup_table/', views.delete_stock_market_lookup_table, name='delete_stock_market_lookup_table'),
    path('update_cookie_crumb_pair/', views.update_cookie_crumb_pair, name='update_cookie_crumb_pair'),
    path('update_stock_ohlcv/<str:stock_symbol>/', views.update_stock_ohlcv, name='update_stock_ohlcv'),
    path('update_all_stock_ohlcv/', views.update_all_stock_ohlcv, name='update_all_stock_ohlcv')]

    