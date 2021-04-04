import requests



def get_Stats():
    BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    #BASE = "http://127.0.0.1:5000/"
    response = requests.get(BASE + "/product/all")
    data = response.json()
    print(data)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

while True:
    success, img = cap.read()
    for barcode in decode(img):
        barcodeNumber = barcode.data.decode('utf-8')
        print(barcodeNumber)

    cv2.imshow('Result', img)
    cv2.waitKey(1)

def addProduct():
    # Product Model {"barcode" : barcode, "name" : name, "price" : price, "quantity" : quantity}
    package = {}
    userInput = input("Enter the barcode of the product : ")
    package["barcode"] = userInput

    userInput = input("Enter the name of the product : ")
    package["name"] = userInput

    while True:
        try:
            userInput = float(input("Enter the price of the product : "))
        except ValueError:
            print("This value needs to be a float")
        else:
            package["price"] = userInput
            break

    while True:
        try:
            userInput = int(input("Enter the quantity of the product in stock : "))
        except ValueError:
            print("This value needs to be a integer")
        else:
            package["quantity"] = userInput
            break

    BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    #BASE = "http://127.0.0.1:5000/"
    response = requests.post(BASE + "/product/add", package)

    return package


print(addProduct())
get_Stats()

def stock():
    print("1 for set\n2 for increase\n3 for decrease")
    userInput = str(input("Enter a Number"))
    BASE = "https://Shopping-System-3.17wilsjam.repl.co"
    #BASE = "http://127.0.0.1:5000/"

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
