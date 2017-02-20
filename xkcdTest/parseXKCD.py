#!/usr/bin/env python

# Parse xkcd image tags

from __future__ import print_function
from builtins import range

import os
import requests

import bs4

def request():
    baseURL = "https://xkcd.com/{0}/"
    if not os.path.exists("xkcdResponses"):
        os.makedirs("xkcdResponses")

    filename = os.path.join("xkcdResponses", "xkcdResponse.{0}.html")
    for i in range(1000, 1001):
        if os.path.isfile(filename.format(i)):
            with open(filename.format(i), "rb") as f:
                content = f.read()
                yield (content, i)
        else:
            response = requests.get(baseURL.format(i))
            content = response.content
            with open(filename.format(i), "wb") as f:
                f.write(content)

            yield (content, i)

def parse(response):
    onlyImgTags = bs4.SoupStrainer("div", {"id": "comic"})
    content = bs4.BeautifulSoup(response, "lxml", parse_only = onlyImgTags)
    # Have to apply a second time - otherwise the doctype is included...
    content = content.findAll(onlyImgTags)
    #print(content)

    for div in content:
        #print(div)
        imgs = div.findAll("img")
        #print(imgs)
        for img in imgs:
            src = img.get("src")
            src = "https:" + src

            # Could probably just return here, since there should only be 1 per page
            #yield src
            return src

def getAndWriteImage(img, imgNumber):
    filename = os.path.join("xkcdResponses", "img", "{0}.png".format(imgNumber))
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    response = requests.get(img)
    if not os.path.isfile(filename):
        with open(filename, "wb") as f:
            f.write(response.content)

if __name__ == "__main__":
    for (response, i) in request():
        img = parse(response)

        getAndWriteImage(img, i)
