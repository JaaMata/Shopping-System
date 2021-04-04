import requests
from barcode import EAN8
from barcode.writer import ImageWriter
import shutil


def barcodeImageGenerator(name, barcodeNumber):
    #BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    BASE = "http://127.0.0.1:5000/"
    response = requests.get(BASE + "/product/all")
    response = response.json()

    x = EAN8(str(barcodeNumber), writer=ImageWriter())
    x.save(f"{name}")
    shutil.move(f'C:/Users/itsem/Desktop/Programming/Python/Shopping-System/{name}.png', 'C:/Users/itsem/Desktop/Programming/Python/Shopping-System/Barcodes/')




# Remote Version
#import requests
#from barcode import EAN8
#from barcode.writer import ImageWriter
#import os, shutil
#
#
#def barcodeImageGenerator(name, barcode):
#    # BASE = "https://Shopping-System-3.17wilsjam.repl.co"
#    BASE = "http://127.0.0.1:5000/"
#    response = requests.get(BASE + "/product/all")
#    response = response.json()
#
#    for i in response:
#        barcodeNumber = response[i]['barcode']
#        x = EAN8(str(barcodeNumber), writer=ImageWriter())
#        name = response[i]['name']
#        x.save(f"{name}")
#
#    shutil.move(f'/some/dir/{name}.png', '/another/dir/Pictures/')


