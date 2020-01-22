import urllib
import json
import utils
import psycopg2

class DataCrawler:
    def __init__(self, config_fname):
        self._config_fname = config_fname

        with open(self._config_fname, "r") as json_file:
            self.data = json.load(json_file)
        

    def get_ticker_names(self, stock_market):
        if stock_market == "bist":
            print(self.data["ticker_symbols_sources"]["bist"])
            utils.get_bist_ticker_names(self.data["ticker_symbols_sources"]["bist"])



dc = DataCrawler(config_fname="/home/ilker/repos/borsa/config/links.json")            
dc.get_ticker_names("bist")