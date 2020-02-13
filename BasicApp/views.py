from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.template import loader
from .models import StockMarket

from lib.data_scraper.get_stock_markets_info import create_stock_market_tables_from_wikipedia
import json
import os

def home(request):

    stock_markets = StockMarket.objects.all()

    template = loader.get_template('home.html')
    context = {'stock_markets': stock_markets}
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

    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets}
    return HttpResponse(template.render(context, request)) 

def update_stock_market_lookup_table(request):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    fname = os.path.join(path,"config","links.json")
    with open(fname) as json_file:
        data = json.load(json_file)

    link = data['list_of_stock_markets_on_wikipedia']

    table_data = create_stock_market_tables_from_wikipedia(link)

    num_samples = len(table_data['name'])

    for i in range(num_samples):
        new_market = StockMarket(market_id=table_data['id'][i], 
                    market_name=table_data['name'][i], 
                    country=table_data['country'][i],
                    city=table_data['city'][i],
                    time_zone=table_data['sort'][i],
                    open_time=table_data['open'][i],
                    close_time=table_data['close'][i],
                    lunch_break=table_data['lunch'][i])
        new_market.save()

    return redirect("/BasicApp/data_manager")    

def create_LookupTablesUpdateStatus_table(request):
    #TODO implement this
    stock_markets = StockMarket.objects.all()

    template = loader.get_template('data_manager.html')
    context = {'stock_markets': stock_markets}

    return redirect("/BasicApp/data_manager")