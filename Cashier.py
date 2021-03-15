import requests
from tkinter import *
from tkinter import messagebox

total = 0

def clear():
    global total
    total = 0
    b.config(text="Barcode:\n")
    n.config(text="Name:\n")
    p.config(text="Price:\n")
    l_price.config(text="Total:\n")
    e_barcode.delete(1)


def getProductInfo(barcode):
    e_barcode.delete(0,100)
    global total
    BASE = "https://Shopping-System-3.17wilsjam.repl.co/"  # For Replit
    #BASE = "http://127.0.0.1:5000/"    # For Pycharm
    response = requests.get(BASE + "product/" + str(barcode))
    if response.json() == False:
        return messagebox.showerror(title="Product Error", message="Product Not Found !")

    data = response.json()
    barcode = data['barcode']
    name = data['name']
    price = data['price']
    total += price
    print(total)
    b.config(text=b['text'] + str(barcode) + "\n")
    n.config(text=n['text'] + str(name) + "\n")
    if str(price)[-1] == "0" and str(price)[-2] == ".":
        f_price = "£" + str(price) + "0"
    if str(total)[-1] == "0" and str(total)[-2] == ".":
        f_total = "£" + str(total) + "0"
    print(f_price)
    p.config(text=p['text'] + str(f_price) + "\n")
    l_price.config(text=f_total)
    return price

root = Tk()

Label(root, text="Barcode").grid(column=1, row=1)
e_barcode = Entry(root)
e_barcode.grid(column=2, row=1)

Label(root,text="Total:").grid(column=2, row=2)
l_price = Label(root, text="")
l_price.grid(column=3, row=2)

Button(root, text="Add Item", command=lambda: getProductInfo(e_barcode.get())).grid(column=2, row=3)
Button(root, text="Clear", command=clear).grid(column=3,row=3)

b = Label(root, text="Barcode:\n")
b.grid(column=1, row=4)
n = Label(root, text="Name:\n")
n.grid(column=2, row=4)
p = Label(root, text="Price:\n")
p.grid(column=3, row=4)
if __name__ == "__main__":
    root.mainloop()