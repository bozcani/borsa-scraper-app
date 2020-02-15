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

        res.append([tickers, name, "https://www.kap.org.tr/"+link])

    return res
