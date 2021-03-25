import requests


# data = {"barcode" : 5901234123457, "name" : "Paper", "price" : 0.05, "quantity" : 49}

#BASE = "https://Shopping-System-2.17wilsjam.repl.co/"
BASE = "http://127.0.0.1:5000/"

# response = requests.post(BASE + "/product/add" , data)

data = {"quantity" : 10, "operation" : "set"}

response = requests.put(BASE + "/product/stock/5901234123457" , data)

response = requests.get(BASE + "/product/all")

