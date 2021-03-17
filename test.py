import requests

data = {"barcode" : 5901234123457, "name" : "Paper", "price" : 0.05, "quantity" : 49}

BASE = "https://Shopping-System-2.17wilsjam.repl.co/"

response = requests.post(BASE + "/product/add" , data)
