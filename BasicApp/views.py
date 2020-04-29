from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.template import loader
from .models import StockMarket, Stock, StockDataLastUpdate, OHLCV, StockDataLastUpdate

from lib.data_scraper.get_tickers_info import get_bist_tickers_info
from lib.data_scraper.get_ohlcv import get_ohlcv_from_yahoo_finance, get_cookie_and_crumb

from datetime import datetime, date, timedelta
import json
import os
import pickle
import requests


def home(request):

    stock_markets = StockMarket.objects.all()
    stocks = Stock.objects.all()

    template = loader.get_template('home.html')
    context = {'stock_markets': stock_markets,
                'stocks': stocks}

    return HttpResponse(template.render(context, request))    


def add_stock_market_result(request):

    market_id = request.GET.get('market_id')
    market_name = request.GET.get('market_name')
    country = request.GET.get('country')
    city = request.GET.get('city')
    time_zone = request.GET.get('time_zone')
    open_time = request.GET.get('open_time')
    close_time = request.GET.get('close_time')
    lunch_break = request.GET.get('lunch_break')

    new_market = StockMarket(market_id=market_id, 
                        market_name=market_name, 
                        country=country,
                        city=city,
                        time_zone=time_zone,
                        open_time=open_time,
                        close_time=close_time,
                        lunch_break=lunch_break)

    new_market.save()
    return redirect("/BasicApp")
                 
def stock_market(request, market_id):
    stock_market = get_object_or_404(StockMarket, pk=market_id)
    context = {
        'stock_market':stock_market,
    }
    return render(request, 'stock_market.html', context)

def delete_stock_market(request,market_id):
    stock_market = get_object_or_404(StockMarket, pk=market_id)

    stock_market.delete()

    return redirect("/BasicApp")

def data_manager(request):

    stock_markets = StockMarket.objects.all()
    log_info=''
    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets,
                'log_info': log_info}
    return HttpResponse(template.render(context, request)) 

def update_stock_market_lookup_table(request):

    # Read json file including info about stock markets.
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    fname = os.path.join(path,"config","stock_markets_info.json")
    with open(fname) as json_file:
        data = json.load(json_file)

    added_markets = []
    skipped_markets = []
    num_samples = len(data)
    for i in range(num_samples):
        if not StockMarket.objects.filter(market_id=data[i]['market_id']).exists():
            new_market = StockMarket(market_id=data[i]['market_id'], 
                        market_name=data[i]['market_name'], 
                        country=data[i]['country'],
                        city=data[i]['city'],
                        time_zone=data[i]['time_zone'],
                        open_time=data[i]['open_time'],
                        close_time=data[i]['close_time'],
                        lunch_break=data[i]['lunch_break'])

            new_market.save()
            added_markets.append(data[i]['market_id'])

        else:
            print(StockMarket.objects.get(market_id=data[i]['market_id']), " exists.")
            skipped_markets.append(data[i]['market_id'])


    log_info = "ADDED MARKETS:\n"
    log_info += ", ".join(added_markets)
    log_info += '\n'
    log_info += "SKIPPED MARKETS (they already exist in the database):\n"
    log_info += ", ".join(skipped_markets)

    stock_markets = StockMarket.objects.all()
    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets,
                'log_info': log_info}
    return HttpResponse(template.render(context, request)) 

def update_stock_lookup_table(request):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    fname = os.path.join(path,"config","links.json")
    with open(fname) as json_file:
        data = json.load(json_file)


    # Get market_id.
    market_id = request.GET.get('market_id')

    added_stocks = []
    skipped_stocks = []
    try:
        link = data['ticker_symbols_sources'][market_id.lower()]
        stock_market = StockMarket.objects.get(market_id=market_id.upper())

        if market_id.lower()=='bist':
            tickers_data = get_bist_tickers_info(link)
            
            for ticker_data in tickers_data:
                if not Stock.objects.filter(stock_symbol=ticker_data[0][0]).exists():
                    new_stock = Stock(stock_symbol = ticker_data[0][0],
                                        stock_market = stock_market,
                                        stock_name = ticker_data[1],
                                        info_link = ticker_data[2])
                    added_stocks.append(ticker_data[0][0])
                    print("Added: ", new_stock )
                    new_stock.save()

                    StockDataLastUpdate(stock=new_stock,
                                        last_update=datetime(1900, 1, 1)).save() # No record


                else:
                    print(Stock.objects.get(stock_symbol=ticker_data[0][0]), " exists.")
                    skipped_stocks.append(ticker_data[0][0])

        log_info = "ADDED STOCKS:\n"
        log_info += ", ".join(added_stocks)
        log_info += '\n'
        log_info += "SKIPPED STOCKS (they already exist in the database):\n"
        log_info += ", ".join(skipped_stocks)


    except KeyError:
        log_info = '{} stock info source is not available in the config file.'.format(market_id)

    stock_markets = StockMarket.objects.all()
    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets,
                'log_info': log_info}
    return HttpResponse(template.render(context, request)) 




def update_cookie_crumb_pair(request):
    cookie, crumb = get_cookie_and_crumb()

    path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    cookie_fname = os.path.join(path,"config","yahoo_finance_cookie")
    crumb_fname = os.path.join(path,"config","yahoo_finance_crumb")

    # Write cookie and crumb binary
    with open(cookie_fname, 'wb') as cookie_file, open(crumb_fname, 'wb') as crumb_file:
        pickle.dump(cookie, cookie_file)
        pickle.dump(crumb, crumb_file)

    time = datetime.now()           

    log_info = "Cookie is updated at time {} with new crumb: {}".format(time, crumb)
    stock_markets = StockMarket.objects.all()
    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets,
                'log_info': log_info}
    return HttpResponse(template.render(context, request)) 

def update_stock_ohlcv(request, stock_symbol):
    print(stock_symbol)

    # Get stock and last update date.
    stocks = Stock.objects.filter(stock_symbol=stock_symbol)

    if len(stocks)==0:
        pass
    else:
        stock = stocks[0]
        last_update = StockDataLastUpdate.objects.filter(stock=stock)[0]
    
        # Prepare yahoo finance cookie and crumb.
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        cookie_fname = os.path.join(path,"config","yahoo_finance_cookie")
        crumb_fname = os.path.join(path,"config","yahoo_finance_crumb")

        with open(cookie_fname, 'rb') as cookie_file, open(crumb_fname, 'rb') as crumb_file:
            cookie = pickle.load(cookie_file)
            crumb = pickle.load(crumb_file)

        # Get ohlcv data.
        start_date = last_update.last_update + timedelta(days=1)
        start_date = "{}-{}-{}".format(start_date.day, start_date.month, start_date.year)
        end_date = date.today()
        end_date = "{}-{}-{}".format(end_date.day, end_date.month, end_date.year)
        try:
            ohlcv_data = get_ohlcv_from_yahoo_finance(stock_symbol, start_date, end_date, cookie, crumb)
        except:
            ohlcv_data = []    

        # Save ohlcv data to the database.
        for data in ohlcv_data:
            ohlcv = OHLCV(date=data['date'],
                            symbol=data['symbol'],
                            open = data['open'],
                            high = data['high'],
                            low = data['low'],
                            close = data['close'],
                            volume = data['volume']
                            )
            ohlcv.save()

        # Update StockDataLastUpdate
        if len(ohlcv_data)!=0:
            last_update.last_update = ohlcv_data[-1]['date']
            last_update.save()

    template = loader.get_template('data_update_status.html')
    last_updates = StockDataLastUpdate.objects.all().order_by("stock_id")
    context = {'last_updates':last_updates}
    return HttpResponse(template.render(context, request))    


def data_update_status(request):
    template = loader.get_template('data_update_status.html')
    last_updates = StockDataLastUpdate.objects.all().order_by("stock_id")
    context = {'last_updates':last_updates}
    return HttpResponse(template.render(context, request))    

def update_all_stock_ohlcv(request):
    stocks = Stock.objects.all()
    for stock in stocks:
        print(stock)
        update_stock_ohlcv(request, stock.stock_symbol)

    template = loader.get_template('data_update_status.html')
    last_updates = StockDataLastUpdate.objects.all()
    context = {'last_updates':last_updates}
    return HttpResponse(template.render(context, request))    



def delete_stock_market_lookup_table(request):

    cnt = StockMarket.objects.count()
    StockMarket.objects.all().delete()

    log_info = "{} stock markets are deleted.".format(cnt)
    stock_markets = StockMarket.objects.all()
    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets,
                'log_info': log_info}
    return HttpResponse(template.render(context, request)) 


def stock_history(request, stock_symbol):
    stock = Stock.objects.filter(stock_symbol=stock_symbol)
    ohlcv_data = OHLCV.objects.filter(symbol=stock_symbol).order_by('-date')
    context = {
        'stock':stock[0],
        'ohlcv_data':ohlcv_data
    }
    return render(request, 'stock_history.html', context)    


# TODO Implement this.
def remove_all_stock_ohlcv_duplicates(request):

    stocks = Stock.objects.all()
    for stock in stocks:
        print(stock)
        remove_stock_ohlcv_duplicates(request, stock.stock_symbol)
   

    template = loader.get_template('data_update_status.html')
    last_updates = StockDataLastUpdate.objects.all()
    context = {'last_updates':last_updates}
    return HttpResponse(template.render(context, request))        


# TODO Implement this.
def remove_stock_ohlcv_duplicates(request, stock_symbol):
    
    print(stock_symbol)
    # Get stock and last update date.
    ohlcv_records = OHLCV.objects.filter(symbol=stock_symbol)

    date_bucket = []
    num_deleted = 0
    if len(ohlcv_records)==0:
        pass
    else:
        for ohlcv in ohlcv_records:
            if ohlcv.date in date_bucket:
                ohlcv.delete()
                num_deleted += 1
            else:
                date_bucket.append(ohlcv.date)    

    print("Duplicates found and deleted: {}".format(num_deleted))
    
    template = loader.get_template('data_update_status.html')
    last_updates = StockDataLastUpdate.objects.all().order_by("stock_id")
    context = {'last_updates':last_updates}
    return HttpResponse(template.render(context, request))    
