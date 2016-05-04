from bs4 import BeautifulSoup
import requests
import ScrapingUtilities
from ScrapingUtilities import *
import sys

class Listings:
    '''scrapes all listings for given city and returns
    list of URLs'''
    def __init__(self, city, state, country):
        # for page 1, extract the listings
        # AND get the max page through which
        # to iterate
        soup = make_soup('https://www.airbnb.com/s/', \
                         city, state, country, 1)
        self.get_max_page(soup)
        self.urls = self.scrape_listing_urls(soup)

        # iterate over remaining pages
        for i in range(2, self.max_page+1):
            soup = make_soup('https://www.airbnb.com/s/', \
                             city, state, country, i)
            u = self.scrape_listing_urls(soup)
            print u
            self.urls.extend(u)

    def get_max_page(self, soup):
        self.max_page = 0
        for p in soup.findAll('div', {'class': 'pagination'}):
            for l in p.findAll('ul', {'class', 'list-unstyled'})[0]\
                      .findAll('li'):
                try:
                    if int(l.text) > self.max_page:
                        self.max_page = int(l.text)
                except:
                    pass
        return self.max_page

    def scrape_listing_urls(self, soup):
        prev = None
        curr = None

        listings = []
        for d in soup.findAll('div', {'class':'listings-container'})[0]\
                     .findAll('div'):
            listings.extend(d.findAll('div', {'class':'listing'}))

        urls = []
        for listing in listings:
            for d in listing.findAll('div'):
                if d.get('class'):
                    prev = curr
                    curr = listing.find('div', {'class':'panel-body'})\
                                   .find('a', {'class', 'text-normal'})
                    if curr and (len(curr) > 0):
                        if not prev:
                            pass
                        elif (curr.get('target') != prev.get('target')): 
                            urls.append(curr.get('href'))         
                else:
                    pass
        return urls