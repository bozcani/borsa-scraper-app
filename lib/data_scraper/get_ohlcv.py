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



def get_cookie(ticker_symbol):
    """Download cookie from Yahoo Finance"""
    url_for_cookie="https://finance.yahoo.com/quote/%s/?p=%s" % (ticker_symbol, ticker_symbol)
    r = requests.get(url_for_cookie, timeout=10)
    cookie = r.cookies    
    return cookie



"""
def _get_crumbs_and_cookies(stock):
    
    #get crumb and cookies for historical data csv download from yahoo finance
    
    #parameters: stock - short-handle identifier of the company 
    
    #returns a tuple of header, crumb and cookie
    
    
    url = 'https://finance.yahoo.com/quote/{}/history'.format(stock)
    with requests.session():
        header = {'Connection': 'keep-alive',
                   'Expires': '-1',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                   }
        
        website = requests.get(url, headers=header, timeout=3)
        soup = BeautifulSoup(website.text, 'lxml')
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', str(soup))

        return (header, crumb[0], website.cookies)



def get_ohlcv_from_yahoo_finance(stock_symbol, start_date, end_date, query_timeout_limit=20):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
    fname = os.path.join(path,"config","links.json")
    with open(fname) as json_file:
        data = json.load(json_file)

    url = data['stock_data_sources']['yahoo_finance']    
    
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

    url = url.replace("TICKER_SYMBOL", stock_symbol)
    url = url.replace("START_PERIOD", str(start_ts))
    url = url.replace("END_PERIOD", str(end_ts))

    print(url)
    # TODO donwload data from the link, and return it.
    
    retrieved = False
    for k in range(query_timeout_limit):

       
        # Get cookie
        url_for_cookie="https://finance.yahoo.com/quote/%s/?p=%s" % (stock_symbol, stock_symbol)
        r = requests.get(url_for_cookie, timeout=100)

        cookie = r.cookies

        with open('cookie', 'wb') as f:
            pickle.dump(cookie, f)
            

        lines = r.content.decode('latin-1').replace('\\', '')
        lines = lines.replace('}', '\n')
        lines = lines.split('\n')
        for l in lines:
            if re.findall(r'CrumbStore', l):
                crumb = '6UV9R8WV2bb'
                print(crumb)
       
        print(k)
        _, crumb, cookie = _get_crumbs_and_cookies(stock_symbol)

        url = url.replace("COOKIECODE", crumb)
        response = requests.get(url, cookies=cookie, timeout=10)

        content = response.content.split(b'\n')

        data = []

        if response.status_code!=200:
            continue

        for c in content[1:]:
            entry = (c.decode("utf-8"))

            if len(entry)<10:
                print('skipped', entry)
                continue
            values = entry.split(',')

            stock_symbol = stock_symbol

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
                            'symbol':stock_symbol, 
                            'date':date,
                            'open':openp,
                            'high':high,
                            'low':low,
                            'close':close,
                            'volume':volume
                        })

        #for block in response.iter_content(1024):
        #    print(block)
        #    print(k)
        print(data)
        print(response.status_code)    
        if response.status_code == 200:
            retrieved = True
            break

    if not retrieved:
        print("Not retrieved")  
        exit()
    else:
        print("OK")    

get_ohlcv_from_yahoo_finance("ISCTR.IS", "12-10-2018", "22-11-2019")
get_ohlcv_from_yahoo_finance("ISCTR.IS", "12-10-2017", "22-11-2019")
get_ohlcv_from_yahoo_finance("ISCTR.IS", "12-10-2016", "22-11-2019")
get_ohlcv_from_yahoo_finance("ISCTR.IS", "12-10-2015", "22-11-2019")
get_ohlcv_from_yahoo_finance("ASELS.IS", "12-10-2015", "22-11-2019")
get_ohlcv_from_yahoo_finance("ASELS.IS", "12-10-2015", "22-11-2019")
get_ohlcv_from_yahoo_finance("ASELS.IS", "12-10-2015", "22-11-2019")
get_ohlcv_from_yahoo_finance("ASELS.IS", "12-10-2015", "22-11-2019")

"""