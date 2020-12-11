import requests
import json
from bs4 import BeautifulSoup


def getItem(stockx):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    r = requests.get(stockx, headers=headers)
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
