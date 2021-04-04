import requests
import pathlib
import cv2
from pyzbar.pyzbar import decode
from time import sleep


def buyProduct(barcode):

    # BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    BASE = "http://127.0.0.1:5000/"
    package = {'operation': 'decrease', 'quantity': 1}
    response = requests.put(BASE + f"/product/stock/{int(barcode)}", package)
    getAll()
    if response.json() == "404":
        return "Invalid Barcode"
    if response.json() == "200":
        return "Item Bought"
    if response.json() == "500":
        return "Server Side Error"
    if not response.json():
        return "Something Went Wrong"

#def manualBarcodeScanner(name):
#    path = pathlib.Path(name + ".png")  # Need to link this to Barcode not the main file
#    if path.exists():
#        img = cv2.imread(f"{str(name)}.png")
#        for code in decode(img):
#            barcodeNumber = code.data.decode('utf-8')
#        return barcodeNumber
#    else:
#        return False


def webCameraScanner():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()
        for barcode in decode(img):
            barcodeNumber = barcode.data.decode('utf-8')
            print(buyProduct(barcodeNumber))
        cv2.imshow('Result', img)
        cv2.waitKey(1)


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


getAll()


#userInput = str(input("Press 1 for manual\n2 For automatic"))
#if userInput == "1":
#    manualBarcodeScanner()
#elif userInput == "2":
#    webCameraScanner()

webCameraScanner()