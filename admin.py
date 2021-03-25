import requests


def get_Stats():
    BASE = "http://127.0.0.1:5000/"
    response = requests.get(BASE + "/product/all")
    data = response.json()
    print(data)


def stock():
    print("1 for set\n2 for increase\n3 for decrease")
    userInput = str(input("Enter a Number"))
    BASE = "http://127.0.0.1:5000/"

    if userInput == "1":
        try:
            userInput = int(input("What do you want the stock to be?"))
        except ValueError:
            print("VALUE ERROR")
        data = {"quantity": userInput, "operation": "set"}
        response = requests.put(BASE + "/product/stock/5901234123457", data)
        get_Stats()

    if userInput == "2":
        try:
            userInput = int(input("What do you want to increase the stock to by?"))
        except ValueError:
            print("VALUE ERROR")
        data = {"quantity": userInput, "operation": "increase"}
        response = requests.put(BASE + "/product/stock/5901234123457", data)
        get_Stats()

    if userInput == "3":
        try:
            userInput = int(input("What do you want to increase the stock to by?"))
        except ValueError:
            print("VALUE ERROR")
        data = {"quantity": userInput, "operation": "decrease"}
        response = requests.put(BASE + "/product/stock/5901234123457", data)
        get_Stats()



userInput = str(input("1 for changing stock prices\nEnter a Number: "))

if userInput == "1":
    stock()
