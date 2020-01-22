import urllib
from bs4 import BeautifulSoup


def get_bist_ticker_names(link_to_source):

    #r = requests.get(link_to_source, "bist-ticker-names.xls")
    #a = urllib.request.urlretrieve(link_to_source)
    a = "tmpp285ccnk"
    a = open(a, "r")
    soup = BeautifulSoup(a, 'html.parser')
    #print(soup.prettify())
    items = soup.findAll("td", {"class":"comp-cell _04 vtable"})

    for item in items:
        
        tickers = item.find("a", {'class': "vcell"}).text.split(",")
        print(tickers)
