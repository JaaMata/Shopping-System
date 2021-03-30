import requests

def getAll():
    BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    response = requests.get(BASE + "/product/all")
    response = response.json()
    for i in response:
        name = response[i]['name']
        barcode = response[i]['barcode']
        price = response[i]['price']
        quantity = response[i]['quantity']

        print(f"Name : {name}\nBarcode : {barcode}\nPrice : {price}\nQuantity : {quantity}\n")

getAll()

while True:
    userProduct = str(input("Please Enter the Barcode of the Product"))