from django.test import TestCase

from django.urls import reverse, resolve
from .views import home, stock_market, delete_stock_market
from .models import StockMarket


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

    def test_home_view_contains_link_to_StockMarketDelete_page(self):
        stock_market_url = reverse('BasicApp:delete_stock_market', kwargs={'market_id': 'TEST'})
        self.assertContains(self.response, 'a href="{}"'.format(stock_market_url[10:])) # Remove "/BasicApp/" from leading.


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
    def test_new_StockMarket_valid_post_data(self):
        url = reverse('BasicApp:add_stock_market_result')
        data = {'market_id':'JUST_CREATED', 
                'market_name':'New stock market',
                'country':'Almanya',
                'city':'Aydin',
                'time_zone':3,
                'open_time':'10:00',
                'close_time':'18:00',
                'lunch_break':'13:00-14:00'}

        response = self.client.get(url, data)
        #for o in StockMarket.objects.all():
        #   print(o)
        #self.assertEquals(response.status_code, 200)    
        #self.assertTrue(StockMarket.objects.filter(pk="JUST_CREATED").exists())
