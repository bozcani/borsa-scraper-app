from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.template import loader
from .models import StockMarket

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

    print(new_market)   

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