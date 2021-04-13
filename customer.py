import requests
import cv2
from pyzbar.pyzbar import decode
from time import sleep


def getAll():
    # BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    BASE = "http://127.0.0.1:5000/"
    response = requests.get(BASE + "/product/all")
    response = response.json()

    for i in response:
        name = response[i]['name']
        barcode = response[i]['barcode']
        price = response[i]['price']
        quantity = response[i]['quantity']

        print(f"Name : {name}\nBarcode : {barcode}\nPrice : {price}\nQuantity : {quantity}\n")


def getInfo(barcode):
    # BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    BASE = "http://127.0.0.1:5000/"
    response = requests.get(BASE + f"/product/{int(barcode)}")
    response = response.json()
    return response


def printReceipt(barcodes):
    receipt = ""
    for i in barcodes:
        data = getInfo(i)
        tempData = f"{data['barcode']}   {data['name']}  {data['price']}\n"
        receipt = receipt + tempData
    print(receipt)


def buyProduct(barcode):
    # BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    BASE = "http://127.0.0.1:5000/"
    package = {'operation': 'decrease', 'quantity': 1}
    response = requests.put(BASE + f"/product/stock/{int(barcode)}", package)
    if response.json() == "404":
        return "Invalid Barcode"
    if response.json() == "200":
        return "Item Bought"
    if response.json() == "500":
        return "Server Side Error"
    if not response.json():
        return "Something Went Wrong"


def breakLoop(x=None):
    if x != None:
        return True


barcodes = []

x = 1

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while x == 1:
    success, img = cap.read()
    for barcode in decode(img):
        barcodeNumber = barcode.data.decode('utf-8')
        barcodes.append(barcodeNumber)
        print(buyProduct(barcodeNumber))
        userInput = str(input("Press Enter to scan another product"))
        if userInput != "":
            x = 2
            break
    cv2.imshow('Result', img)
    cv2.waitKey(1)

print(barcodes)

printReceipt(barcodes)
