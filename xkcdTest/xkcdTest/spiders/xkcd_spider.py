#!/usr/bin/env python

# Test scraping the XKCD website
# We'll rate limit to be considerate!

from __future__ import print_function
#from builtins import range

import scrapy
from bs4 import BeautifulSoup

class XKCDSpider(scrapy.Spider):
    name = "xkcdSpider"
    onlyImgTags = bs4.SoupStrainer("img")

    def start_requests(self):
        baseURL = "https://xkcd.com/{0}/"

        for i in range(1000, 1001):
        #for i in range(1000, 1010):
            yield scrapy.Request(url=baseURL.format(i), callback=self.parse)

    def parse(self, response):
        imgRes = BeautifulSoup(response, parse_only=onlyImgTags)
        for img in imgRes:
            pass

# Example for the tutorial page
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
            self.log('Saved file %s' % filename)

if __name__ == "__main__":
    pass
