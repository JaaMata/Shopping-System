import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "product/5901234123457")
print(response.json())

response = requests.get(BASE + "product/all")
print(response.json())
