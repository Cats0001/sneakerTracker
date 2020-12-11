from api import getItem
import pickle

class item:
    def __init__(self, stockx, size, initial):
        if not initial:
            self.data = getItem(stockx)
            self.stockx = stockx
            size = size.upper()
            if size not in self.data['sizes']:
                raise ValueError('Size not found!')
            else:
                self.size = size

            self.value = self.data['sizes'][self.size]['price']
            self.getPayout()
        else:
            self.stockx = stockx
            self.size = size

    def refresh(self, data):
        if data is not None:
            self.data = data
        else:
            self.data = getItem(self.stockx)
        self.value = self.data['sizes'][self.size]['price']
        self.getPayout()
        return self.data

    def getPayout(self):
        self.payout = round(self.value*0.915, 2)  # hardcoded 8.5% for now


class itemList:
    def __init__(self):
        self.data = []

    def add(self, stockx, size, initial):
        self.data.append(item(stockx, size, initial))

    def listItems(self):
        i=1
        totalPrice = 0
        totalPayout = 0
        print('ID - NAME - SIZE - PRICE - PAYOUT')
        for product in self.data:
            print(f'[{i}] {product.data["item"]["name"]} - {product.size} - ${product.value} - ${product.payout}')
            totalPrice += product.value
            totalPayout += product.payout
            i+=1

        print()
        print(f'Total Value: ${totalPrice}.00')
        print(f'Total Payout: ${round(totalPayout,2)}')

    def refreshAll(self):
        i = 1
        cache = {
        }
        for product in self.data:
            if product.stockx in cache:
                d = product.refresh(cache[product.stockx])
            else:
                d = product.refresh(None)
            print(f'[{i}] refreshed')
            cache[product.stockx] = d
            i+=1

    def save(self):
        products = []
        for product in self.data:
            products.append([product.stockx, product.size])

        pickle.dump(products, open('items.dat', 'wb'))

    def load(self):
        try:
            products = pickle.load(open('items.dat', 'rb'))
        except:
            products = []

        for product in products:
            self.add(product[0], product[1], True)
        self.refreshAll()

    def remove(self, indice):
        self.data.pop(indice)


items = itemList()
items.load()

while True:
    inp = input("(a)dd, (l)ist, (r)efresh, (d)elete, (e)xit:  ").lower()
    if inp == 'a':
        inp = input("stockX URL:  ").lower()
        inp2 = input("size:   ").lower()
        items.add(inp, inp2, False)
        items.save()
    elif inp == 'l':
        items.listItems()
    elif inp == 'r':
        items.refreshAll()
    elif inp == 'd':
        inp = input("item:   ")
        items.remove(int(inp)-1)
        items.save()
    elif inp == 'e':
        items.save()
        exit(0)