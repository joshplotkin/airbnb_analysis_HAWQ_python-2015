from bs4 import BeautifulSoup
import requests
import sys

def make_soup(base, city = None, state = None, country = None, i = None):
    if city:
        city = city.replace(' ','%20')
        country = country.replace(' ','-')
        url = base + city + '--' + state + '--' + country + '?page=' + str(i)
    else:
        url = base
    print url
    tree = requests.get(url).text
    soup = BeautifulSoup(tree, 'lxml')

    if '503' in soup.findAll('title')[0].text:
        print 'Error code: 503; Airbnb is temporarily unavailable'
        sys.exit(0)

    return soup