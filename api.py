import requests
import json
from bs4 import BeautifulSoup
from hyper.contrib import HTTP20Adapter

s = requests.session()
s.mount('https://stockx.com', HTTP20Adapter())


def getItem(stockx):
    headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
            }
    r = s.get(stockx, headers=headers)
    data = BeautifulSoup(r.text, "lxml")
    div = data.find("div", {"class": "product-view"})
    scripts = div.find_all("script", {"type":"application/ld+json"})
    itemData = json.loads(scripts[0].string)
    itemInfo = {
        'item':
            {'name': itemData['name'],
             'releaseDate': itemData['releaseDate'],
             'brand': itemData['brand'],
             'sku': itemData['sku'],
             'color': itemData['color']
             },
        'sizes': {

        }
    }

    for offer in itemData['offers']['offers']:
        itemInfo['sizes'][offer['description']] = {
            'sku': offer['sku'],
            'price': offer['price'],
            'size': offer['description']
        }

    return itemInfo
