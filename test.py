from random import randint
import requests
from time import sleep
from math import ceil

def checkBarcode(barcode):
    checkDigit = str(barcode)[-1]
    lst = []
    checkNum = [3, 1, 3, 1, 3, 1, 3]
    total = 0
    for i in str(barcode):
        lst.append(i)

    for i in range(7):
        total = total + int(lst[i]) * checkNum[i]

    roundedTotal = ceil(int(total) / 10.0) * 10
    total = roundedTotal - total

    if int(total) == int(checkDigit):
        return True
    else:
        return False

print(checkBarcode(30927100))


#BASE = "https://Shopping-System-3.17wilsjam.repl.co"
BASE = "http://127.0.0.1:5000"


names = ["eggs", "milk", "bread", "ice cream", "flour", "tea bags", "rat poison", "chocolate", "steak", "pork"]

prices = [4.50, 3.25, 6.42, 10.00, 3.00, 2.40, 0.99, 4.30, 5.00, 6.00]

package = {}

for i in range(10):
    package['barcode'] = "gen"
    package['name'] = names[i]
    package['price'] = prices[i]
    package['quantity'] = randint(1,200)

    print(package)

    response = requests.post(BASE + "/product/add", package)
    sleep(0.5)
    package = {}