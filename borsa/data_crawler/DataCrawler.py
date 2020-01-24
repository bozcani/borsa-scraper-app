import urllib
import json
import utils
import psycopg2


class DataCrawler:
    def __init__(self, config_fname):
        self._config_fname = config_fname

        with open(self._config_fname, "r") as json_file:
            self.data = json.load(json_file)
        

    def get_ticker_symbols(self, stock_market):
        if stock_market == "bist":
            tickers = utils.get_bist_tickers(self.data["ticker_symbols_sources"]["bist"])
            return tickers



dc = DataCrawler(config_fname="/home/ilker/repos/borsa/config/links.json")            
tickers = dc.get_ticker_symbols("bist")


print(tickers)