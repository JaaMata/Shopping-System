import requests

barcode = ""

# BASE = "http://0.0.0.0:8080/"  # For Replit
BASE = "http://127.0.0.1:5000/"  # For Pycharm
response = requests.get(BASE + "checkproduct?barcode=" + str(barcode))
print(response.json())

response = requests.get(BASE + "?barcode=" + str(barcode))
print(response.json())



