import requests
from Barcodes import BarcodeScaner
import cv2  # Read image / camera
from pyzbar.pyzbar import decode

from Barcodes.BarcodeScaner import barcodeScanner


def buyProduct(barcode, quantity):
    # BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    BASE = "http://127.0.0.1:5000/"
    package = {'operation' : 'decrease'}
    package['quantity'] = int(quantity)
    response = requests.put(BASE + f"/product/stock/{int(barcode)}", package)

    if response.json() == "404":
        return "Invalid Barcode"
    if response.json() == "200":
        return "Item Bought"
    if response.json() == "500":
        return "Server Side Error"
    if not response.json():
        return "Something Went Wrong"

def getAll():
   #BASE = "https://Shopping-System-3.17wilsjam.repl.co"
   BASE = "http://127.0.0.1:5000/"
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
   productName = str(input("Please Enter the Name of the Product You Would Like To Buy : "))
   if productName != "":
       break

if barcodeScanner(productName) != False:
    while True:
        try:
            userProduct = int(input("Please Enter the Quantity of the Product You Would Like To Buy : "))
        except ValueError:
            print("Please only use numbers")
        else:
            buyProduct(productName, userProduct)
            break

