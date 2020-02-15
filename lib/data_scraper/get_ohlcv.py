import urllib
import json
import urllib.request as urllib
from bs4 import BeautifulSoup
import os
import datetime
import calendar

def date_to_unixtimestamp(date_str):
    """DD-MM-YEAR to Unix timestamp"""

    date_list = date_str.split('-')
    day = int(date_list[0])
    month = int(date_list[1])
    year = int(date_list[2])

    d = datetime.date(year,month,day)
    unix_timestamp = calendar.timegm(d.timetuple())
    return unix_timestamp


def get_ohlcv_from_yahoo_finance(stock_symbol, start_date, end_date):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
    fname = os.path.join(path,"config","links.json")
    with open(fname) as json_file:
        data = json.load(json_file)

    link = data['stock_data_sources']['yahoo_finance']    
    t = datetime.datetime.fromtimestamp(1581379200)
    print(t)

    print(stock_symbol, start_date, end_date, link)

#get_ohlcv_from_yahoo_finance("ISCTR", 0, 1)

