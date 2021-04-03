import pathlib
import cv2
from pyzbar.pyzbar import decode

def barcodeScanner(name):

    path = pathlib.Path(name+".png")    # Need to link this to Barcode not the main file
    if path.exists():
        img = cv2.imread(f"{str(name)}.png")
        for code in decode(img):
            barcodeNumber = code.data.decode('utf-8')
        return barcodeNumber
    else:
        return False
