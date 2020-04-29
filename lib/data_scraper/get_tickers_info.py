import urllib.request as urllib
from bs4 import BeautifulSoup


def get_bist_tickers_info(link_to_source):

    #r = requests.get(link_to_source, "bist-ticker-names.xls")
    a = urllib.urlretrieve(link_to_source)
    #print(a)
    #a = ("tmpp285ccnk",3)
    a = open(a[0], "r")
    soup = BeautifulSoup(a, 'html.parser')
    #print(soup.prettify())
    items = soup.findAll("td", {"class":"comp-cell _04 vtable"})
    names = soup.findAll("td", {"class":"comp-cell _14 vtable"})

    res = []
    for item,name in zip(items,names):
        
        tickers = item.find("a", {'class': "vcell"}).text.split(",")
        tickers = [ticker.strip() for ticker in tickers]
        
        name = name.find("a", {'class': "vcell"}).text.split(",")
        name = ''.join(str(elem) for elem in name)

        link = item.find("a",href=True).get("href")

        res.append([[ticker+'.IS' for ticker in tickers], name, "https://www.kap.org.tr/"+link])

    return res


def get_bist_indexes_info(link_to_source):

    a = urllib.urlretrieve(link_to_source)
    a = open(a[0], "r")
    soup = BeautifulSoup(a, 'html.parser')
    items = soup.findAll("a", {"class":"w-inline-block sub-leftresultbox"})

    res = []
    for item in items:
        name = item.find("div", {'class': "type-normal bold"}).text
        symbol = item.findAll("div", {'class': "type-normal"})[1].text
        info = item.find("div", {'class': "type-xsmall"}).text
        res.append({"symbol":symbol+'.IS', 
                    "name":name, 
                    "info":info})
    return res