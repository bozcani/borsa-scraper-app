import urllib
import json
import urllib.request as urllib
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_stock_exchange_trading_hours"

from ..BasicApp.models import StockMarket

def create_stock_market_tables_from_wikipedia(url):

    a = urllib.urlretrieve(url)
    a = open(a[0], "r")

    soup = BeautifulSoup(a, 'html.parser')

    table = soup.find('table', attrs={'class':'wikitable sortable'})
    table_body = table.find('tbody')

    data={
        "name":[],
        "id":[],
        "country":[],
        "city":[],
        "zone":[],
        "sort":[],
        "dst":[],
        "open":[],
        "close":[],
        "lunch":[],
        "utc_open":[],
        "utc_close":[],
        "utc_lunch":[],
    }

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cols = [ele for ele in cols if ele]
        if len(cols)==13:
            for i in range(13):
                data[list(data.keys())[i]].append(cols[i])

        elif len(cols)==12:
            cols.insert(6, None)
            for i in range(13):
                data[list(data.keys())[i]].append(cols[i])
  


create_stock_market_tables_from_wikipedia(url)