import urllib
import json
import urllib.request as urllib
from bs4 import BeautifulSoup
import os
import datetime
import calendar
import urllib.request
import requests
import re
import pickle

def date_to_UXtimestamp(date_str):
    """DD-MM-YEAR to Unix timestamp"""

    date_list = date_str.split('-')
    day = int(date_list[0])
    month = int(date_list[1])
    year = int(date_list[2])

    d = datetime.date(year,month,day)
    unix_timestamp = calendar.timegm(d.timetuple())
    return unix_timestamp



def get_cookie_and_crumb(ticker_symbol='GOOGL'):
    """Download cookie from Yahoo Finance"""
    url_for_cookie = 'https://finance.yahoo.com/quote/{}/history'.format(ticker_symbol)

    with requests.session():
        header = {'Connection': 'keep-alive',
                    'Expires': '-1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                    }

        r = requests.get(url_for_cookie, headers=header, timeout=10)
        soup = BeautifulSoup(r.text, 'lxml')
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))
        cookie = r.cookies    
        return cookie, crumb[0]



def get_ohlcv_from_yahoo_finance(ticker_symbol, start_date, end_date, cookie, crumb):


    # Convert daytime to unix timestamp.
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

    # Get data from Yahoo Finance.
    url = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}".format(ticker_symbol, start_ts, end_ts, crumb)

    response = requests.get(url, cookies=cookie, timeout=10)
    content = response.content.split(b'\n')

    if response.status_code!=200:
        print(response.content)
        raise RuntimeError("Cookie does not work: {}".format(response.status_code))

    data = []
    for c in content[1:]:
        entry = (c.decode("utf-8"))

        if len(entry)<10:
            print('skipped', entry)
            continue
        values = entry.split(',')

        date = datetime.date(int(values[0].split('-')[0]), int(values[0].split('-')[1]), int(values[0].split('-')[2]))
        
        if values[1] == 'null':
            openp = -1
        else:    
            openp = float(values[1])

        if values[2]=='null':
            high = -1
        else:
            high = float(values[2])

        if values[3]=='null':
            low = -1
        else:
            low = float(values[3])    

        if values[4]=='null':
            close = -1
        else:    
            close = float(values[4])

        if values[6]=='null':    
            volume = -1
        else:
            volume = int(values[6])

        data.append({
                        'symbol':ticker_symbol, 
                        'date':date,
                        'open':openp,
                        'high':high,
                        'low':low,
                        'close':close,
                        'volume':volume
                    })

    return data