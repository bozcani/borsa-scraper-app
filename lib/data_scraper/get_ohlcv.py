import urllib
import json
import urllib.request as urllib
from bs4 import BeautifulSoup
import os
import datetime
import calendar

def date_to_UXtimestamp(date_str):
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
    
    if start_date == 'beginning':
        start_ts = 0
    else:    
        start_ts = date_to_UXtimestamp(start_date)
    
    if end_date == 'today':
        end_date = datetime.datetime.now()
        end_date = "{}-{}-{}".format(end_date.day, end_date.month, end_date.year)
        end_ts = date_to_UXtimestamp(end_date)
    else:
        end_ts = date_to_UXtimestamp(end_date)

    link = link.replace("TICKER_SYMBOL", stock_symbol)
    link = link.replace("START_PERIOD", str(start_ts))
    link = link.replace("END_PERIOD", str(end_ts))

    print(link)
    # TODO donwload data from the link, and return it.


