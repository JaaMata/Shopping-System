from random import randint
import requests
from time import sleep

BASE = "https://Shopping-System-3.17wilsjam.repl.co"
BASE = "http://127.0.0.1:5000/"

names = ["Eggs", "Milk", "Bread", "Ice cream", "Flour", "Tea Bags", "Rat Poison", "Chocolate", "Steak", "Pork"]

prices = [4.50, 3.25, 6.42, 10.00, 3.00, 2.40, 0.99, 4.30, 5.00, 6.00]

package = {}

for i in range(10):
    package['barcode'] = "gen"
    package['name'] = names[i]
    package['price'] = prices[i]
    package['quantity'] = randint(1,200)

    print(package)
    
    response = requests.post(BASE + "/product/add", package)
    sleep(0.1)
    package = {}