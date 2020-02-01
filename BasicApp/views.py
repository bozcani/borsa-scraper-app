from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import StockMarket

def home(request):

    template = loader.get_template('home.html')
    context = {}
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

    print(new_market)   

    new_market.save()
    return HttpResponse("hello")   
                 
    #new_person.save()
    #context = {
    #    'first_name':first_name,
    #    'last_name':last_name,
    #    'birthdate':birthdate
    #}        