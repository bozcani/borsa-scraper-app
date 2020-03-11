from django.test import TestCase, Client

from django.urls import reverse, resolve
from .views import home, stock_market, delete_stock_market, data_manager, data_update_status
from .models import StockMarket, Stock, OHLCV, StockDataLastUpdate
import datetime

class HomeTests(TestCase):
    def setUp(self):
        StockMarket.objects.create(market_id='TEST', 
                                    market_name='Test stock market',
                                    country='Turkey',
                                    city='Buharkent',
                                    time_zone=3,
                                    open_time='10:00',
                                    close_time='18:00',
                                    lunch_break='13:00-14:00')
        url = reverse('BasicApp:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('BasicApp:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/BasicApp/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_StockMarketDetail_page(self):
        stock_market_url = reverse('BasicApp:stock_market', kwargs={'market_id': 'TEST'})
        self.assertContains(self.response, 'a href="{}"'.format(stock_market_url[10:])) # Remove "/BasicApp/" from leading.

    """
    def test_home_view_contains_link_to_StockMarketDelete_page(self):
        stock_market_url = reverse('BasicApp:delete_stock_market', kwargs={'market_id': 'TEST'})
        self.assertContains(self.response, 'a href="{}"'.format(stock_market_url[10:])) # Remove "/BasicApp/" from leading.
    """

    def test_new_StockMarket_post_data_success_status_code(self):
        url = reverse('BasicApp:home')
        data = {'market_id':'JUST_CREATED2', 
                'market_name':'New stock market',
                'country':'Almanya',
                'city':'Aydin',
                'time_zone':3,
                'open_time':'10:00',
                'close_time':'18:00',
                'lunch_break':'13:00-14:00'}

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)    


class StockMarketTests(TestCase):
    def setUp(self):
        StockMarket.objects.create(market_id='TEST', 
                                    market_name='Test stock market',
                                    country='Turkey',
                                    city='Buharkent',
                                    time_zone=3,
                                    open_time='10:00',
                                    close_time='18:00',
                                    lunch_break='13:00-14:00')

    
    def test_StockMarket_view_success_status_code(self):
        url = reverse('BasicApp:stock_market', kwargs={'market_id': 'TEST'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_StockMarket_view_not_found_status_code(self):
        url = reverse('BasicApp:stock_market', kwargs={'market_id': 'TEST-NOEXIST'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_StockMarket_url_resolves_new_topic_view(self):
        view = resolve('/BasicApp/stock_market/TEST/')
        self.assertEquals(view.func, stock_market)        

    def test_StockMarket_view_contains_link_back_to_homepage(self):
        url = reverse('BasicApp:stock_market', kwargs={'market_id': 'TEST'})
        response = self.client.get(url)
        homepage_url = reverse('BasicApp:home')
        self.assertContains(response, 'href="{}"'.format(homepage_url))

class AddStockMarket(TestCase):
    def setUp(self):
        self.form_data = {'market_id':'JUST_CREATED', 
                'market_name':'New stock market',
                'country':'Almanya',
                'city':'Aydin',
                'time_zone':3,
                'open_time':'10:00',
                'close_time':'18:00',
                'lunch_break':'13:00-14:00'}

    def test_new_StockMarket_valid_get_data(self):
        url = reverse('BasicApp:add_stock_market_result')
        response = self.client.get(url, self.form_data)
        self.assertTrue(StockMarket.objects.filter(pk="JUST_CREATED").exists())

    def test_new_StockMarket_view_success_status_code(self):
        url = reverse('BasicApp:add_stock_market_result')
        response = self.client.get(url, self.form_data)
        self.assertEquals(response.status_code, 302)    


class DataManagerTests(TestCase):
    def setUp(self):
        StockMarket.objects.create(market_id="TEST", 
                                    market_name='Test stock market',
                                    country='Turkey',
                                    city='Buharkent',
                                    time_zone=3,
                                    open_time='10:00',
                                    close_time='18:00',
                                    lunch_break='13:00-14:00')

    
    def test_DataManager_view_success_status_code(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_DataManager_url_resolves_new_topic_view(self):
        view = resolve('/BasicApp/data_manager/')
        self.assertEquals(view.func, data_manager)   

    def test_UpdateStockMarketsLookupTable_button_exist(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        button_link = reverse('BasicApp:update_stock_market_lookup_table')
        self.assertContains(response, "action=\"{}\"".format(button_link))

    def test_UpdateStockLookupTable_button_exist(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        button_link = reverse('BasicApp:update_stock_lookup_table')
        self.assertContains(response, "action=\"{}\"".format(button_link))

    
    def test_DeleteStockMarketsLookupTable_button_exist(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        button_link = reverse('BasicApp:delete_stock_market_lookup_table')
        self.assertContains(response, "action=\"{}\"".format(button_link))

    def test_UpdateCookieCrumbPair_button_exist(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        button_link = reverse('BasicApp:update_cookie_crumb_pair')
        self.assertContains(response, "action=\"{}\"".format(button_link))

    def test_view_contains_link_back_to_homepage(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        homepage_url = reverse('BasicApp:home')
        self.assertContains(response, 'href="{}"'.format(homepage_url))     

    def test_drop_down_menu_exist(self):
        url = reverse('BasicApp:data_manager')
        response = self.client.get(url)
        self.assertContains(response, 'option value=\"TEST\"')     


class DataUpdateStatusTests(TestCase):
    def setUp(self):
        StockMarket.objects.create(market_id='SAMPLE_STOCK_MARKET', 
                                    market_name='Test stock market',
                                    country='Turkey',
                                    city='Buharkent',
                                    time_zone=3,
                                    open_time='10:00',
                                    close_time='18:00',
                                    lunch_break='13:00-14:00')

        Stock.objects.create(stock_symbol='SAMPLE_STOCK', 
                                    stock_name='Test stock market',
                                    stock_market=StockMarket.objects.filter(market_id='SAMPLE_STOCK_MARKET')[0],
                                    info_link='emtpy_link')

        """
        OHLCV.objects.create(date=datetime.datetime(1993, 6, 16),
                            stock_symbol="SAMPLE_STOCK",
                            open = 1.,
                            high = 1.,
                            low = 1.,
                            close = 1.,
                            volume = 1)   
        """

        StockDataLastUpdate.objects.create(stock=Stock.objects.get(stock_symbol='SAMPLE_STOCK'),
                                            last_update=datetime.datetime(2020,2,2))                 
    
    def test_DataUpdateStatus_view_success_status_code(self):
        url = reverse('BasicApp:data_update_status')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_DataUpdateStatus_url_resolves_new_topic_view(self):
        view = resolve('/BasicApp/data_update_status/')
        self.assertEquals(view.func, data_update_status)   

    def test_view_contains_link_back_to_homepage(self):
        url = reverse('BasicApp:data_update_status')
        response = self.client.get(url)
        homepage_url = reverse('BasicApp:home')
        self.assertContains(response, 'href="{}"'.format(homepage_url)) 

    def test_view_contains_updateAll_button(self):
        url = reverse('BasicApp:data_update_status')
        response = self.client.get(url)
        button_link = reverse('BasicApp:update_all_stock_ohlcv')
        self.assertContains(response, "a href=\"{}\"".format(button_link))

    def test_view_history_button(self):
        url = reverse('BasicApp:data_update_status')
        response = self.client.get(url)
        button_link = reverse('BasicApp:stock_history', kwargs={'stock_symbol': 'SAMPLE_STOCK'})
        self.assertContains(response, "a href=\"{}\"".format(button_link))

    def test_view_updateohlcv_button(self):
        url = reverse('BasicApp:data_update_status')
        response = self.client.get(url)
        button_link = reverse('BasicApp:update_stock_ohlcv', kwargs={'stock_symbol': 'SAMPLE_STOCK'})
        self.assertContains(response, "a href=\"{}\"".format(button_link))